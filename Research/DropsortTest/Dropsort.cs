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

namespace DropsortTest
{
    public class Dropsort
    {
        private List<int> randomArray;
        private List<int> sortedArray;
        private int TEST_SIZE = 1000;
        private TimeSpan span;
        private DateTime before;
        private DateTime after;
        public int millis;

        public Dropsort(double randomness)
        {
            millis = 0;
            randomArray = new List<int>();
            Random rand = new Random((int)DateTime.Now.Ticks);
            for (int i = 0; i < TEST_SIZE; i++)
            {
                randomArray.Add(i);
            }
            for (int i = 0; i < TEST_SIZE; i++)
            {
                if (rand.NextDouble() < randomness)
                {
                //    int removed = randomArray[i];
                //    randomArray.RemoveAt(i);
                //    randomArray.Insert(rand.Next(randomArray.Count), removed);
                    randomArray[i] = rand.Next(randomArray.Count);
                }
            }
        }

        public void initArray()
        {
            sortedArray = new List<int>();
        }

        public int checkSort()
        {
            for (int i = 1; i < sortedArray.Count; i++)
            {
                if (sortedArray[i] < sortedArray[i - 1])
                {
    //                System.Console.WriteLine("Array is not sorted!");
                    return -1;
                }
            }
 //           System.Console.WriteLine("Size: " + sortedArray.Count + " (" + ((double)sortedArray.Count) / ((double)TEST_SIZE) * 100 + " percent filled)");
            return sortedArray.Count;
         //   millis += span.Milliseconds;
    //        return span.Milliseconds;
        }

        public void quickSort()
        {
             before = DateTime.Now;

            sortedArray = randomArray;
            sortedArray.Sort();

             after = DateTime.Now;
             span = after - before;
    //        System.Console.WriteLine("time: " + span.Milliseconds);
        }

        public void originalSort()
        {
             before = DateTime.Now;

            int previousInt = -1;
            for (int i = 0; i < TEST_SIZE; i++)
            {
                if (randomArray[i] >= previousInt)
                {
                    sortedArray.Add(randomArray[i]);
                    previousInt = randomArray[i];
                }
            }

            after = DateTime.Now;
            span = after - before;
   //         System.Console.WriteLine("time: " + span.Milliseconds);
        }

        public void doubleSort()
        {
             before = DateTime.Now;

            int previousInt = -1;
            for (int i = 0; i < TEST_SIZE; i++)
            {
                if (randomArray[i] >= previousInt)
                {
                    if (i + 1 < randomArray.Count && randomArray[i] <= randomArray[i + 1])
                    {
                        sortedArray.Add(randomArray[i]);
                        previousInt = randomArray[i];
                    }
                }
            }

             after = DateTime.Now;
             span = after - before;
   //         System.Console.WriteLine("time: " + span.Milliseconds);
        }

        public void memorySort(int recency)
        {
             before = DateTime.Now;

            int age = 0;
            int previousInt = -1;
            for (int i = 0; i < TEST_SIZE; i++)
            {
                if (randomArray[i] >= previousInt)
                {
                    sortedArray.Add(randomArray[i]);
                    previousInt = randomArray[i];
                }
                else
                {
                    age++;
                    if (age >= recency && sortedArray.Count != 1)
                    {
                        // drop the int we added last, and restart sorting
                        // with the next int after that
                        // i -= age;//removed this because it makes it n^2 worst case
                        sortedArray.RemoveAt(sortedArray.Count - 1);
                        age = 0;
                        previousInt = sortedArray[sortedArray.Count - 1];
                    }
                }
            }

             after = DateTime.Now;
             span = after - before;
 //           System.Console.WriteLine("time: " + span.Milliseconds);
        }

        public void doubleMemorySort(int recency)
        {
             before = DateTime.Now;

            int age = 0;
            int previousInt = -1;
            int localMaximum = -1;
            for (int i = 0; i < TEST_SIZE; i++)
            {
                if (randomArray[i] >= previousInt)
                {
                    if ((i + 1 < randomArray.Count) && randomArray[i] <= randomArray[i + 1])
                    {
                        sortedArray.Add(randomArray[i]);
                        previousInt = randomArray[i];
                    }
                }
                else
                {
                    age++;
                    if (age >= recency && sortedArray.Count != 1)
                    {
                        // drop the int we added last, and restart sorting
                        // with the next int after that
                        // i -= age;//removed this because it makes it n^2 worst case
                        sortedArray.RemoveAt(sortedArray.Count - 1);
                        age = 0;
                        previousInt = sortedArray[sortedArray.Count - 1];
                    }
                }
            }

             after = DateTime.Now;
             span = after - before;
   //         System.Console.WriteLine("time: " + span.Milliseconds);
        }
    }
}
