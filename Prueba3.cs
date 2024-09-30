using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        // Configuración del servidor
        int port = 12345;

        // Crear un punto de conexión
        IPEndPoint localEndPoint = new IPEndPoint(IPAddress.Any, port);

        // Crear un socket TCP/IP
        Socket listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        // Vincular el socket al punto de conexión y escuchar conexiones entrantes
        listener.Bind(localEndPoint);
        listener.Listen(10);

        Console.WriteLine("Esperando conexiones...");

        while (true)
        {
            // Aceptar una conexión entrante
            Socket handler = listener.Accept();

            // Mostrar información sobre la conexión entrante
            Console.WriteLine($"Conexión aceptada desde {handler.RemoteEndPoint}");

            // Recibir datos del cliente
            byte[] buffer = new byte[1024];
            int bytesRecibidos = handler.Receive(buffer);
            string data = Encoding.ASCII.GetString(buffer, 0, bytesRecibidos);
            Console.WriteLine($"Mensaje del cliente: {data}");

            // Responder al cliente
            string respuesta = "Hola desde C#";
            byte[] msg = Encoding.ASCII.GetBytes(respuesta);
            handler.Send(msg);

            // Cerrar la conexión
            handler.Shutdown(SocketShutdown.Both);
            handler.Close();
        }
    }
}

