import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class client {
    static Thread sent;
    static Thread receive;
    static Socket socket;

    public static void main(String args[]) {
        try {
            socket = new Socket("localhost", 9999);
        } catch (UnknownHostException e1) {
            e1.printStackTrace();
        } catch (IOException e1) {
            e1.printStackTrace();
        }

        sent = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    BufferedReader stdIn = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    BufferedReader userInput =  new BufferedReader(new InputStreamReader(System.in));
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    while (true) {
                        out.print(userInput.readLine() + "\r\n");
                        out.flush();
                        System.out.println("Trying to read...");
                        String in = stdIn.readLine();
                        System.out.println(in);
                    }

                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

            }
        });
        sent.start();
        try {
            sent.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}