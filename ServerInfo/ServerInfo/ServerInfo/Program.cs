using System.Diagnostics;
using System.Globalization;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using CommandLine;
using System.Linq;
using System.Reflection.Metadata;
using System;
using System.ComponentModel;
using System.Collections.Concurrent;
using System.Reflection;

namespace ServerInfo
{
    internal class Program
    {
        // REQUIRED CONSTS

        const int PROCESS_QUERY_INFORMATION = 0x0400;
        const int MEM_COMMIT = 0x00001000;
        const int PAGE_READWRITE = 0x04;
        const int PROCESS_WM_READ = 0x0010;

        // REQUIRED METHODS

        [DllImport("kernel32.dll")]
        public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);

        [DllImport("kernel32.dll")]
        static extern bool ReadProcessMemory(IntPtr handle, IntPtr addy, byte[] buffer, int size, out int bytesRead);

        [DllImport("kernel32.dll")]
        static extern uint GetLastError();

        [DllImport("kernel32.dll", SetLastError = true)]
        static extern int VirtualQueryEx(IntPtr hProcess, IntPtr lpAddress, out MEMORY_BASIC_INFORMATION lpBuffer, uint dwLength);

        [DllImport("kernel32.dll")]
        static extern void GetSystemInfo(out SYSTEM_INFO lpSystemInfo);

        public class CommandLineOptions
        {
            [Option(shortName: 'o', Required = false, Default = null)]
            public string OutputPath { get; set; }

            [Option(shortName: 'p', Required = false, Default = "FoxGame")]
            public string ProcessNameFilter { get; set; }

            [Option(shortName: 'u', Required = false, Default = 5000)]
            public int UpdateRate { get; set; }

            [Option(shortName: 's', Required = false, Default = true)]
            public bool SelectNewest { get; set; }
        }

        static void Main(string[] args)
        {
            var arguments = Parser.Default.ParseArguments<CommandLineOptions>(args).Value;

            if (string.IsNullOrWhiteSpace(arguments.OutputPath))
                arguments.OutputPath = Path.Combine(Directory.GetCurrentDirectory(), "output");

            DirectoryInfo outputDirectory = Directory.CreateDirectory(arguments.OutputPath);

            string outputFile = Path.Combine(outputDirectory.FullName, "player_list.json");

            Console.WriteLine($"Output file: {outputFile}");

            var processes = new List<Process>();

            Console.WriteLine("Finding processes");
            while (processes.Count == 0)
            {
                processes = new List<Process>(Process.GetProcesses().Where(x => x.ProcessName.Contains(arguments.ProcessNameFilter)));
                Console.WriteLine("...");
                Thread.Sleep(1000);
            }

            processes = processes.OrderByDescending(x => x.StartTime).ToList();

            foreach (var (process, i) in processes.Select((x, i) => (x, i)))
            {
                Console.WriteLine($"{i}:{process.ProcessName} (ID:{process.Id}, StartTime:{process.StartTime})");
            }

            Process selectedProcess = processes.First();

            if (processes.Count > 1 && !arguments.SelectNewest)
            {
                int input = -1;

                while (input < 0 || input >= processes.Count)
                {
                    Console.WriteLine("Select process:");
                    int.TryParse(Console.ReadLine(), out input);
                }

                selectedProcess = processes[input];
            }

            Console.WriteLine($"Selected:{selectedProcess.ProcessName} (ID:{selectedProcess.Id}, StartTime:{selectedProcess.StartTime})");
            
            Console.WriteLine("Press Q to quit");

            var timer = new System.Threading.Timer(
                (x) => { Update(outputFile, selectedProcess); },
                null,
                TimeSpan.FromSeconds(5),
                TimeSpan.FromSeconds(5));

            while (true)
            {
                if (Console.ReadKey(true).Key == ConsoleKey.Q) break;
            }
            timer.Dispose();
        }

        private static void Update(string outputFile, Process selectedProcess)
        {
            Stopwatch stopwatch = new Stopwatch();
            stopwatch.Start();
            var playerAddresses = ScanPlayers(selectedProcess);
            //Console.WriteLine($"ScanPlayers : {stopwatch.ElapsedMilliseconds}ms");

            var playerNames = new List<string>();
            var botNames = new List<string>();

            foreach (IntPtr ptr in playerAddresses)
            {
                string? name = GetPlayerName(selectedProcess, ptr);
                string? ip = GetPlayerIP(selectedProcess, ptr);
                //Console.WriteLine($"{name}:{ip}");
                if (name != null && !string.IsNullOrWhiteSpace(ip))
                    playerNames.Add(name);
                else if (name != null && string.IsNullOrWhiteSpace(ip))
                    botNames.Add(name);
            }

            //Console.WriteLine("Players:");
            foreach (var name in playerNames)
            {
                //Console.WriteLine(name);
            }

            //Console.WriteLine("Bots:");
            foreach (var name in botNames)
            {
                //Console.WriteLine(name);
            }


            string contents = $"{{\"PlayerCount\": {playerNames.Count}, \"PlayerList\": [";

            foreach (var name in playerNames)
            {
                contents += $"\"{name}\",";
            }
            contents = contents.TrimEnd(',');
            contents += "]}";

            try
            {
                File.WriteAllText(outputFile, contents);
            }
            catch
            {
                Console.WriteLine($"Failed to write to file: {outputFile}");
            }
            //Console.WriteLine($"Update : {stopwatch.ElapsedMilliseconds}ms | Players : {playerNames.Count}");
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct MEMORY_BASIC_INFORMATION
        {
            public IntPtr BaseAddress;
            public IntPtr AllocationBase;
            public uint AllocationProtect;
            public IntPtr RegionSize;
            public uint State;
            public uint Protect;
            public uint Type;
        }

        public struct SYSTEM_INFO
        {
            public ushort processorArchitecture;
            ushort reserved;
            public uint pageSize;
            public IntPtr minimumApplicationAddress;
            public IntPtr maximumApplicationAddress;
            public IntPtr activeProcessorMask;
            public uint numberOfProcessors;
            public uint processorType;
            public uint allocationGranularity;
            public ushort processorLevel;
            public ushort processorRevision;
        }

        public static List<IntPtr> ScanPlayers(Process proc)
        {
            // opening the process with desired access level
            IntPtr processHandle =
            OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_WM_READ, false, proc.Id);

            SYSTEM_INFO sys_info = new SYSTEM_INFO();
            GetSystemInfo(out sys_info);

            IntPtr proc_min_address = sys_info.minimumApplicationAddress;
            IntPtr proc_max_address = sys_info.maximumApplicationAddress;

            // saving the values as long ints so I won't have to do a lot of casts later
            long proc_min_address_l = (long)proc_min_address;
            long proc_max_address_l = (long)proc_max_address;

            MEMORY_BASIC_INFORMATION mem_basic_info = new MEMORY_BASIC_INFORMATION();
            List<MEMORY_BASIC_INFORMATION> memList = new List<MEMORY_BASIC_INFORMATION>();

            uint memSize = (uint)Marshal.SizeOf(typeof(MEMORY_BASIC_INFORMATION));

            while (proc_min_address_l < proc_max_address_l)
            {
                int memDump = VirtualQueryEx(processHandle, proc_min_address, out mem_basic_info, memSize);
                if (memDump == 0)
                {
                    var err = GetLastError();
                    throw new Exception("GetMemoryInfo failed : GetLastError() : " + new Win32Exception((int)err).Message);
                }

                // if this memory chunk is accessible
                if (mem_basic_info.Protect ==
                PAGE_READWRITE && mem_basic_info.State == MEM_COMMIT)
                {
                    memList.Add(mem_basic_info);
                }

                // move to the next memory chunk
                proc_min_address_l += (long)mem_basic_info.RegionSize;
                proc_min_address = new IntPtr(proc_min_address_l);
            }

            string playerPattern = "20 32 77 01";
            int alignment = 0x100;

            int[] intlist = TransformArray(playerPattern);

            int maxBufferSize = (int)memList.Max(i => i.RegionSize);
            int rangeSize = 1000;
            List<IntPtr> results = new List<IntPtr>();

            Parallel.ForEach(Partitioner.Create(0, memList.Count(), rangeSize), range =>
            {
                var buffer = new byte[maxBufferSize];
                for (var index = range.Item1; index < range.Item2; index++)
                {
                    var item = memList[index];
                    ReadProcessMemory(processHandle, item.BaseAddress, buffer, (int)item.RegionSize, out _);
                    var result = PatternScan(intlist, buffer, (int)item.RegionSize, (long)item.BaseAddress, alignment);
                    results.AddRange(result);
                }
            });

            return results;
        }
        public static string? GetPlayerName(Process proc, IntPtr playerAddress)
        {
            List<int> pointerOffsets = new List<int>() { 0x9c, 0x1EC };
            return GetStringUTF16(proc, playerAddress, pointerOffsets);
        }
        public static string? GetPlayerIP(Process proc, IntPtr playerAddress)
        {
            List<int> pointerOffsets = new List<int>() { 0x9c, 0x234 };
            return GetStringUTF16(proc, playerAddress, pointerOffsets);
        }

        static List<IntPtr> PatternScan(int[] intlist, byte[] buffer, long bufferSize, long offset, int alignment = 0x1)
        {
            var results = new List<IntPtr>();

            for (int a = 0; a < bufferSize; a += alignment)
            {
                for (int b = 0; b < intlist.Length; b++)
                {
                    if (a + b >= bufferSize || (intlist[b] != -1 && intlist[b] != buffer[a + b]))
                        break;
                    if (b + 1 == intlist.Length)
                    {
                        var result = new IntPtr(a + offset);
                        results.Add(result);
                    }
                }
            }
            return results;
        }

        static int[] TransformArray(string sig)
        {
            var bytes = sig.Split(' ');
            int[] intlist = new int[bytes.Length];

            for (int i = 0; i < intlist.Length; i++)
            {
                if (bytes[i] == "??")
                    intlist[i] = -1;
                else
                    intlist[i] = int.Parse(bytes[i], NumberStyles.HexNumber);
            }
            return intlist;
        }

        public static string? GetStringUTF16(Process proc, IntPtr playerAddress, List<int> pointerOffsets)
        {
            var ptr = NavigatePointerList(proc, playerAddress, pointerOffsets);
            if (ptr != null)
                return ReadStringUTF16(proc, ptr.Value);
            return "ERROR";
        }

        public static IntPtr? NavigatePointerList(Process proc, IntPtr baseAddress, List<int> pointerOffsets)
        {
            IntPtr newPtr = baseAddress;
            foreach (var ptr in pointerOffsets)
            {
                var value = ReadInt32(proc, newPtr + ptr);
                if (value == null) return null;
                newPtr = new IntPtr(value.Value);
            }
            return newPtr;
        }
        public static int? ReadInt32(Process proc, IntPtr address)
        {
            if (address == IntPtr.Zero) return null;
            byte[] buffer = new byte[4];
            ReadProcessMemory(proc.Handle, address, buffer, buffer.Length, out _);

            return BitConverter.ToInt32(buffer, 0);
        }
        public static string? ReadStringUTF16(Process proc, IntPtr address, int maxLength = 32)
        {
            if (address == IntPtr.Zero) return null;
            byte[] buffer = new byte[maxLength * 2];
            ReadProcessMemory(proc.Handle, address, buffer, buffer.Length, out _);

            for (int i = 0; i < buffer.Length; i += 2)
            {
                if (buffer[i] == 0x0 && buffer[i + 1] == 0x0)
                    return Encoding.Unicode.GetString(buffer, 0, i);
            }
            return Encoding.Unicode.GetString(buffer);
        }

    }
}