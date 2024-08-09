using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

namespace weather_lamp
{
    public static class GetWeatherFunction
    {
        [FunctionName("GetWeather")]
        public static async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            if (req.Headers["special-key"] != "OogZC#PFD$OxYgfXWZigj6Zh7a4gvRk0")
            {
                return new OkResult();
            }

            var http = new HttpClient();

            var apikey = "d125a24ba4091a423306b2ac7357b01b";
            
            string response = await http.GetStringAsync($"https://api.openweathermap.org/data/2.5/onecall?lat=-33.81667&lon=151.0&units=metric&exclude=current,minutely,daily,alerts&appid={apikey}");

            var data = Welcome3.FromJson(response);
            
            var oneToFourHours = data.Hourly.Take(4);
            var fourToEightHours = data.Hourly.Skip(4).Take(4);

            var oneToFourHourlyAverages = new
            {
                averageTemp = Math.Round(oneToFourHours.Average(h => h.Temp), 2),
                averagePrecip = Math.Round(oneToFourHours.Max(h => h.Pop), 2),
                averageCloudCover = 0
            };

            var fourToEightHourlyAverages = new
            {
                averageTemp = Math.Round(fourToEightHours.Average(h => h.Temp), 2),
                averagePrecip = Math.Round(fourToEightHours.Max(h => h.Pop), 2),
                averageCloudCover = 0
            };

            var result = new
            {
                oneToFourHours = oneToFourHourlyAverages,
                fourToEightHours = fourToEightHourlyAverages
            };

            return new OkObjectResult(result);
        }
    }
}
