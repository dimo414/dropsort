/*
Copyright 2016 Abram Jackson
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace DropsortTest
{
    class Program
    {
        static void Main(string[] args)
        {
            Dropsort dropsort;
            TextWriter write = new StreamWriter(@"results.csv");


            for (double j = 0.0; j < 1; j += .01)
            {
                dropsort = new Dropsort(j);
                System.Console.WriteLine("Original");
                double average = 0;
     //           dropsort.millis = 0;
                DateTime before = DateTime.Now;
                for (int i = 0; i < 1000; i++)
                {
                              dropsort = null;
                                 dropsort = new Dropsort(j);
                    dropsort.initArray();
                    dropsort.originalSort();
                    average += dropsort.checkSort();
                }
                DateTime after = DateTime.Now;
                TimeSpan span = after - before;
    //            System.Console.WriteLine("time: " + (int)Math.Round(average / 1000) + "; " + dropsort.millis);
                write.Write((int)Math.Round(average / 1000.0) + ",");

                //ROUND NOT CAST YA DOOFUS

                average = 0;
                dropsort.millis = 0;
                before = DateTime.Now;
                System.Console.WriteLine("\nMemory");
                for (int i = 0; i < 1000; i++)
                {
                                dropsort = null;
                                dropsort = new Dropsort(j);
                    dropsort.initArray();
                    dropsort.memorySort(4);
                    average += dropsort.checkSort();
                }
                after = DateTime.Now;
                span = after - before;
    //            System.Console.WriteLine("time: " + (int)Math.Round(average / 1000) + "; " + dropsort.millis);

                write.Write((int)Math.Round(average / 1000.0) + ",");

                average = 0;
                dropsort.millis = 0;
                System.Console.WriteLine("\nDouble");
                before = DateTime.Now;
                for (int i = 0; i < 1000; i++)
                {
                                dropsort = null;
                                dropsort = new Dropsort(j);
                    dropsort.initArray();
                    dropsort.doubleSort();
                    average += dropsort.checkSort();
                }
                after = DateTime.Now;
                span = after - before;
     //           System.Console.WriteLine("time: " + (int)Math.Round(average / 1000) + "; " + dropsort.millis);
                write.Write((int)Math.Round(average / 1000.0) + ",");


                System.Console.WriteLine("\nDouble Memory");
                average = 0;
                dropsort.millis = 0;
                before = DateTime.Now;
                for (int i = 0; i < 1000; i++)
                {
                               dropsort = null;
                               dropsort = new Dropsort(j);
                    dropsort.initArray();
                    dropsort.doubleMemorySort(4);
                    average += dropsort.checkSort();
                }
                after = DateTime.Now;
                span = after - before;
        //        System.Console.WriteLine("time: " + (int)Math.Round(average / 1000) + "; " + dropsort.millis);
                write.Write((int)Math.Round(average / 1000.0) + ",");
                write.WriteLine();
                //}
                //          write.Close();

                /*           TextWriter write = new StreamWriter(@"results.csv");
                           for (int i = 1; i <= 10; i++)
                           {

                               for (int j = 0; j <= 100; j += 10)
                               {
                                   average = 0;
                                   for (int k = 0; k < 1000; k++)
                                   {
                                       dropsort = null;
                                       dropsort = new Dropsort( ((double)j) / 100.0);
                                       dropsort.initArray();
                                       dropsort.memorySort((int)Math.Pow(2,i));
                                       average += dropsort.checkSort();
                                   }
                                   write.Write((int)Math.Round(average / 1000.0) + ",");

                               }
                               write.WriteLine();
                           }
                           write.Close();
                           System.Console.Write("Average: " + (int)average / 1000);
            
                           // 1, 2, 15, 5, 7, 3, 6, 10
                           //
                           /*
                           System.Console.WriteLine("\nQuicksort");
                           dropsort.millis = 0;
                           before = DateTime.Now;
                           for (int i = 0; i < 1000; i++)
                           {
                       //        dropsort = null;
                      //         dropsort = new Dropsort(.3);
                               dropsort.initArray();
                               dropsort.quickSort();
                               dropsort.checkSort();
                               average += dropsort.checkSort();
                           }
                           after = DateTime.Now;
                           span = after - before;
                           System.Console.WriteLine("time: " + (int)Math.Round(average / 1000) + "; " + dropsort.millis);
                 //          write.Write((int)Math.Round(average / 1000.0) + ",");
                           */
            }
            write.Close();
            System.Console.WriteLine("done");
        }
    }
}
