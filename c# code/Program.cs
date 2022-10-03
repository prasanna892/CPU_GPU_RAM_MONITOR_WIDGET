using System.Collections.Generic;
using OpenHardwareMonitor.Hardware;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using System.Diagnostics;

namespace HWmonitor
{
    public class Program
    {
        /**
         * Init OpenHardwareMonitor.dll Computer Object
         **/
        static Computer computer = new Computer()
        {
            GPUEnabled = true,
            CPUEnabled = true,
            RAMEnabled = true,
            MainboardEnabled = true,
            HDDEnabled = true,
        };

        
        /**
         *  Define vars to hold stats
         **/
        public static string result = "";
        public static List<string> CPUclock = new List<string>(){"***************Clocks***************"};
        public static List<string> CPUtemp = new List<string>(){"*************Temperature*************"};
        public static List<string> CPUload = new List<string>(){"*****************Load****************"};
        public static List<string> CPUpower = new List<string>(){"***************Power****************"};
        public static List<List<string>> CPUlist = new List<List<string>>();

        public static List<string> GPUclock = new List<string>(){"***************Clocks***************"};  
        public static List<string> GPUtemp = new List<string>(){"*************Temperature*************"};
        public static List<string> GPUload = new List<string>(){"*****************Load****************"};
        public static List<string> GPUpower = new List<string>(){"***************Power****************"};
        public static List<string> GPUdata = new List<string>(){"*****************Data****************"};
        public static List<List<string>> GPUlist = new List<List<string>>();

        public static List<string> RAMload = new List<string>(){"*****************Load****************"};
        public static List<string> RAMdata = new List<string>(){"*****************Data****************"};
        public static List<List<string>> RAMlist = new List<List<string>>();

        public static List<List<List<string>>> allList = new List<List<List<string>>>(){CPUlist, GPUlist, RAMlist};

        public static Dictionary<string, Dictionary<string, Dictionary<string, string>>> hardwareDict = new Dictionary<string, Dictionary<string, Dictionary<string, string>>>();
        public static Dictionary<string, Dictionary<string, string>> hardwareTypeDict = new Dictionary<string, Dictionary<string, string>>();
        public static Dictionary<string, string> hardwarePropertiesDict = new Dictionary<string, string>(); 

        static bool CPUprint1;
        static bool GPUprint1;
        static bool RAMprint1;
        static bool CPUFound;
        static bool GPUFound;
        static bool RAMFound;
        static bool oneShot = true;

        [DllImport("kernel32.dll")]
        static extern IntPtr GetConsoleWindow();

        [DllImport("User32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int cmdShow);

        /**
         * Converting list to dictionary
         **/
        public static void dictConvert(List<List<string>> list, string hardwareType_) {
            hardwarePropertiesDict.Add("Name", list.ElementAt(0).ElementAt(0));
            foreach (var items in list) {
                foreach (var item in items) {
                    if (items.Count > 1) {
                        String[] val = item.Split(':');
                        if (val.Length == 2) {
                            hardwarePropertiesDict.Add(val[0], val[1]);
                        }
                    }
                }

                Dictionary<string, string> hardwarePropertiesDictN = new Dictionary<string, string>(hardwarePropertiesDict); 
                if (items.Count > 1 || items.ElementAt(0).Contains('*')) {
                    hardwareTypeDict.Add(items[0], hardwarePropertiesDictN);
                } else { 
                    hardwareTypeDict.Add("Name", hardwarePropertiesDictN);
                }
                hardwarePropertiesDict.Clear();
            }
            Dictionary<string, Dictionary<string, string>> hardwareTypeDictN = new Dictionary<string, Dictionary<string, string>>(hardwareTypeDict); 
            hardwareTypeDict.Clear();
            hardwareDict.Add(hardwareType_, hardwareTypeDictN);
        }

        /**
         * Writting all data to write.txt file
         **/
        public static void TXTList(List<List<string>> list, bool val = true) {
            bool firstRun = true;
            try {
                using(StreamWriter writetext = new StreamWriter("result.txt", val)) {
                    foreach (var items in list) {
                        foreach (var item in items) {
                            if (items.Count > 1) {
                                writetext.WriteLine("   "+item);
                            }
                            if (firstRun) {
                                writetext.WriteLine(item);
                                firstRun = false;
                            }
                        }
                    }
                }
            } catch {
                // pass
            }
        }

        /**
         * Clear previous data
         **/
        public static void listClear() {
            foreach (var list in allList) {
                foreach (var items in list) {
                    items.RemoveRange(1, items.Count-1);
                }
                list.Clear();
            }
        }

        /**
         * Pulls data from OpenHardwareMonitor.dll
         **/
        public static void ReportSystemInfo() {
            if (oneShot) {
                computer.Open();
                oneShot = false;
            }
            CPUprint1 = true;
            GPUprint1 = true;
            RAMprint1 = true;
            CPUFound = true;
            GPUFound = true;
            RAMFound = true;
            foreach (var hardware in computer.Hardware) {
                hardware.Update();
                
                foreach (var sensor in hardware.Sensors) {
                    if (hardware.HardwareType == HardwareType.CPU) {
                        if (CPUprint1) {
                            CPUFound = false;
                            CPUlist.Add(new List<string>{hardware.Name});
                            CPUprint1 = false;
                        }
                        if (sensor.SensorType == SensorType.Clock) {
                            CPUclock.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " MHz");
                        } else if (sensor.SensorType == SensorType.Temperature) {
                            CPUtemp.Add(sensor.Name + ":" + sensor.Value.GetValueOrDefault(0) + " °C");
                        } else if (sensor.SensorType == SensorType.Load) {
                            CPUload.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " %");
                        } else if (sensor.SensorType == SensorType.Power) {
                            CPUpower.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " W");
                        }
                    }
                }

                foreach (var sensor in hardware.Sensors) {
                    if (sensor.Name.Contains("GPU")) {
                        if (GPUprint1) {
                            GPUFound = false;
                            GPUlist.Add(new List<string>{hardware.Name});
                            GPUprint1 = false;
                        }
                        if (sensor.SensorType == SensorType.Clock) {
                            GPUclock.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " MHz");
                        } else if (sensor.SensorType == SensorType.Temperature) {
                            GPUtemp.Add(sensor.Name + ":" + sensor.Value.GetValueOrDefault(0) + " °C");
                        } else if (sensor.SensorType == SensorType.Load) {
                            GPUload.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " %");
                        } else if (sensor.SensorType == SensorType.Power) {
                            GPUpower.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " W");
                        } else if (sensor.SensorType == SensorType.SmallData) {
                            GPUdata.Add(sensor.Name + ":" +  Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " MB");
                        }
                    }
                }

                foreach (var sensor in hardware.Sensors) {
                    if (hardware.HardwareType == HardwareType.RAM) {
                        if (RAMprint1) {
                            RAMFound = false;
                            RAMlist.Add(new List<string>{hardware.Name});
                            RAMprint1 = false;
                        }
                        if (sensor.SensorType == SensorType.Load) {
                            RAMload.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " %");
                        } else if (sensor.SensorType == SensorType.Data) {
                            RAMdata.Add(sensor.Name + ":" + Math.Round(sensor.Value.GetValueOrDefault(0), 1) + " GB");
                        }
                    }
                }
            }
            /**
            * Add sub-list to main-list
            **/
            if (CPUFound) {
                CPUlist.Add(new List<string>{"CPU Not Found"});
            }
            if (GPUFound) {
                GPUlist.Add(new List<string>{"GPU Not Found"});
            }
            if (RAMFound) {
                RAMlist.Add(new List<string>{"RAM Not Found"});
            }
            CPUlist.Add(CPUclock);
            CPUlist.Add(CPUtemp);
            CPUlist.Add(CPUload);
            CPUlist.Add(CPUpower);

            GPUlist.Add(GPUclock);
            GPUlist.Add(GPUtemp);
            GPUlist.Add(GPUload);
            GPUlist.Add(GPUpower);
            GPUlist.Add(GPUdata);

            RAMlist.Add(RAMload);
            RAMlist.Add(RAMdata);
        }

        /**
         * Get more information from OpenHardwareMonitor.dll
         **/
        public static void MoreInfo() {
            try {
                using (TextWriter textWriter = new StreamWriter("MoreInfo.txt"))
                {
                    var report = computer.GetReport().Split('\n').Skip(3);
                    textWriter.Write(string.Join("\n", report));
                }
            } catch {
                // pass
            }
        }

        /**
        * Getting full error details
        **/
        public static string GetAllFootprints(Exception x) {
            var st = new StackTrace(x, true);
            var frames = st.GetFrames();
            var traceString = new StringBuilder();

            foreach (var frame in frames) {
                if (frame.GetFileLineNumber() < 1)
                    continue;

                traceString.Append("File: " + frame.GetFileName());
                traceString.Append(", Method:" + frame.GetMethod().Name);
                traceString.Append(", LineNumber: " + frame.GetFileLineNumber());
                traceString.Append("  -->  ");
            }

            return traceString.ToString();
        }

        /**
        * Main method
        **/
        static void Main(string[] args) {
            var handle = GetConsoleWindow();
            ShowWindow(handle, 0);  // set to 5 for show window

            // loop
            while (true) {
                try {
                    ReportSystemInfo();
                    dictConvert(CPUlist, "CPU");
                    dictConvert(GPUlist, "GPU");
                    dictConvert(RAMlist, "RAM");
                    string json = JsonConvert.SerializeObject(hardwareDict, Formatting.Indented);
                    try {
                        File.WriteAllText("result.json", json);
                    } catch {
                        // pass
                    }
                    hardwareDict.Clear();
                    TXTList(CPUlist, false);
                    TXTList(GPUlist);
                    TXTList(RAMlist);
                    listClear();
                    MoreInfo();
                    Thread.Sleep(500);
                } catch (Exception ex) {
                    using(StreamWriter writetext = new StreamWriter("resultErrLog.txt")) {
                        writetext.Write(GetAllFootprints(ex));
                    }
                }
            }
        }
    }
}