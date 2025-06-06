// Filename: KafkaConnectionCheck.cs

using System;
using Confluent.Kafka;

class Program
{
    static void Main()
    {
        var config = new ProducerConfig
        {
            BootstrapServers = "YOUR_BOOTSTRAP_SERVER",       // e.g. pkc-xxx.us-east-1.aws.confluent.cloud:9092
            SaslMechanism = SaslMechanism.Plain,
            SecurityProtocol = SecurityProtocol.SaslSsl,
            SaslUsername = "YOUR_CLIENT_ID",                  // API Key / Client ID
            SaslPassword = "YOUR_CLIENT_SECRET",              // API Secret / Client Secret
            ClientId = "ConnectionTestClient"                 // Optional: use your own tag
        };

        try
        {
            using var producer = new ProducerBuilder<Null, string>(config).Build();
            // Try a metadata fetch
            var metadata = producer.GetMetadata(TimeSpan.FromSeconds(5));
            Console.WriteLine("✅ Successfully connected to Kafka broker!");
            Console.WriteLine("Broker count: " + metadata.Brokers.Count);
        }
        catch (Exception ex)
        {
            Console.WriteLine("❌ Connection failed: " + ex.Message);
        }
    }
}
