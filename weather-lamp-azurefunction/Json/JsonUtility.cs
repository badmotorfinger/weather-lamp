using System;
using System.Globalization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace weather_lamp
{
    public enum Main { Clear, Clouds, Rain };

    public partial class Welcome3
    {
        public static Welcome3 FromJson(string json) => JsonConvert.DeserializeObject<Welcome3>(json, Converter.Settings);
    }

    public static class Serialize
    {
        public static string ToJson(this Welcome3 self) => JsonConvert.SerializeObject(self, Converter.Settings);
    }

    internal static class Converter
    {
        public static readonly JsonSerializerSettings Settings = new JsonSerializerSettings
        {
            MetadataPropertyHandling = MetadataPropertyHandling.Ignore,
            DateParseHandling = DateParseHandling.None,
            Converters =
            {
                MainConverter.Singleton,
                new IsoDateTimeConverter { DateTimeStyles = DateTimeStyles.AssumeUniversal }
            },
        };
    }

    internal class MainConverter : JsonConverter
    {
        public override bool CanConvert(Type t) => t == typeof(Main) || t == typeof(Main?);

        public override object ReadJson(JsonReader reader, Type t, object existingValue, JsonSerializer serializer)
        {
            if (reader.TokenType == JsonToken.Null) return null;
            var value = serializer.Deserialize<string>(reader);
            switch (value)
            {
                case "Clear":
                    return Main.Clear;
                case "Clouds":
                    return Main.Clouds;
                case "Rain":
                    return Main.Rain;
            }
            throw new Exception("Cannot unmarshal type Main");
        }

        public override void WriteJson(JsonWriter writer, object untypedValue, JsonSerializer serializer)
        {
            if (untypedValue == null)
            {
                serializer.Serialize(writer, null);
                return;
            }
            var value = (Main)untypedValue;
            switch (value)
            {
                case Main.Clear:
                    serializer.Serialize(writer, "Clear");
                    return;
                case Main.Clouds:
                    serializer.Serialize(writer, "Clouds");
                    return;
                case Main.Rain:
                    serializer.Serialize(writer, "Rain");
                    return;
            }
            throw new Exception("Cannot marshal type Main");
        }

        public static readonly MainConverter Singleton = new MainConverter();
    }
}

