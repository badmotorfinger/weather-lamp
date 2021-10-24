using System.Collections.Generic;

namespace weather_lamp
{
    public class Hourly
    {
        public string Summary { get; set; }
        public string Icon { get; set; }
        public List<HourlyForecast> Data { get; set; }
    }
}