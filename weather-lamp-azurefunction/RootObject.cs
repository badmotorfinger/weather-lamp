namespace weather_lamp
{
    public class RootObject
    {
        public double Latitude { get; set; }
        public double Longitude { get; set; }
        public string Timezone { get; set; }
        public Currently Currently { get; set; }
        public Hourly Hourly { get; set; }
        public int Offset { get; set; }
    }
}