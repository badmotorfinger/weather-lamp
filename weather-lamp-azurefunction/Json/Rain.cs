using Newtonsoft.Json;

namespace weather_lamp
{
    public partial class Rain
    {
        [JsonProperty("1h")]
        public double The1H { get; set; }
    }
}