using Newtonsoft.Json;

namespace weather_lamp
{
    public partial class Welcome3
    {
        [JsonProperty("lat")]
        public double Lat { get; set; }

        [JsonProperty("lon")]
        public long Lon { get; set; }

        [JsonProperty("timezone")]
        public string Timezone { get; set; }

        [JsonProperty("timezone_offset")]
        public long TimezoneOffset { get; set; }

        [JsonProperty("hourly")]
        public Hourly[] Hourly { get; set; }
    }
}