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
            if (req.Headers["special-key"] != "a random key to protect your azure function")
            {
                return new OkResult();
            }

            var http = new HttpClient();

            string response = await http.GetStringAsync("https://api.darksky.net/forecast/your darksky API key goes here/-33.808996764,151.000666664?exclude=minutely,flags&units=si");

            RootObject data = JsonConvert.DeserializeObject<RootObject>(response);

            IEnumerable<HourlyForecast> oneToFourHours = data.Hourly.Data.Take(4);
            IEnumerable<HourlyForecast> fourToEightHours = data.Hourly.Data.Skip(4).Take(4);

            var oneToFourHourlyAverages = new
            {
                averageTemp = oneToFourHours.Average(h => h.Temperature),
                averagePrecip = oneToFourHours.Max(h => h.PrecipProbability)
            };

            var fourToEightHourlyAverages = new
            {
                averageTemp = fourToEightHours.Average(h => h.Temperature),
                averagePrecip = fourToEightHours.Max(h => h.PrecipProbability)
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
