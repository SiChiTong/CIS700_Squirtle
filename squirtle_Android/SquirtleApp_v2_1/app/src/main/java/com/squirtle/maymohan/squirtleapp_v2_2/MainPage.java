package com.squirtle.maymohan.squirtleapp_v2_2;
// REFERENCE: https://wingoodharry.wordpress.com/2014/03/15/simple-android-to-arduino-via-bluetooth-serial-part-2/

import android.app.Activity;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.UUID;

public class MainPage extends Activity {
    boolean button_flag = false;
    TextView tView;
    TextView dynamicText;
    Button yesBut;
    //Member Fields
    private BluetoothAdapter btAdapter = null;
    private BluetoothSocket btSocket = null;
    private OutputStream outStream = null;
    private InputStream inStream = null;

    // private ConnectedThread mConnectedThread;
    // UUID service - This is the type of Bluetooth device that the BT module is
    // It is very likely yours will be the same, if not google UUID for your manufacturer
    private static final UUID MY_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    // MAC-address of Bluetooth module
    public String newAddress = null;

    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_page);

// TextView initializations
        tView = (TextView) findViewById(R.id.tview);
        dynamicText = (TextView) findViewById(R.id.modeText);
        yesBut = (Button) findViewById(R.id.yesButton);
        //getting the bluetooth adapter value and calling checkBTstate function
        btAdapter = BluetoothAdapter.getDefaultAdapter();
        checkBTState();
    }

    // All bluetooth connection stuff done here so even if app is paused this can be redone
    @Override
    public void onResume() {
        super.onResume();
        // connection methods are best here in case program goes into the background etc

        //Get MAC address from DeviceListActivity
        Intent intent = getIntent();
        newAddress = intent.getStringExtra(LandingPage.EXTRA_DEVICE_ADDRESS);

        // Set up a pointer to the remote device using its address.
        BluetoothDevice device = btAdapter.getRemoteDevice(newAddress);

        //Attempt to create a bluetooth socket for comms
        try {
            btSocket = device.createRfcommSocketToServiceRecord(MY_UUID);
        } catch (IOException e1) {
            Toast.makeText(getBaseContext(), "ERROR - Could not create Bluetooth socket", Toast.LENGTH_SHORT).show();
            System.err.println("ah-Ha!");
        }

        // Establish the connection.
        try {
            btSocket.connect();
        } catch (IOException e) {
            try {
                btSocket.close();        //If IO exception occurs attempt to close socket
            } catch (IOException e2) {
                Toast.makeText(getBaseContext(), "ERROR - Could not close Bluetooth socket", Toast.LENGTH_SHORT).show();
            }
        }
        // Create a data stream so we can talk to the device
        try {
            outStream = btSocket.getOutputStream();
        } catch (IOException e) {
            Toast.makeText(getBaseContext(), "ERROR - Could not create bluetooth outstream", Toast.LENGTH_SHORT).show();
        }
        InputStream tmpIn = null;
        //OutputStream tmpOut = null;

        try {
            //Create I/O streams for connection
            tmpIn = btSocket.getInputStream();
            // tmpOut = socket.getOutputStream();
        } catch (IOException e) {
        }
        inStream = tmpIn;

        //When activity is resumed, attempt to send a piece of junk data ('x') so that it will fail if not connected
        // i.e don't wait for a user to press button to recognise connection failure
        //sendData("x\n");


        Thread workerThread = new Thread(new Runnable() {
            @Override
            public void run() {
                byte[] buffer = new byte[256];
                int bytes;

                // Keep looping to listen for received messages
                while (true) {
                    try {
                        bytes = inStream.read(buffer);            //read bytes from input buffer
                        String readMessage = new String(buffer, 0, bytes);
                        textChange(readMessage);
                    } catch (IOException e) {
                        break;
                    }
                }
            }
        });
        workerThread.start();

    }

    public void textChange(String msg) {
        final String str = msg;
        final String[] temp = str.split(" ");
        final String currentTask = temp[0];
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                //sendData("I am nuts!!");
                android.os.Process.setThreadPriority(10);
                tView.setText(currentTask);
                if (currentTask.equals("go_to_room")) {
                    dynamicText.setText(getString(R.string.squirtleNav) + temp[1]);
                    yesBut.setVisibility(View.GONE);
                } else if (currentTask.equals("find_person")) {
                    dynamicText.setText(getString(R.string.squirtleRetr) + temp[1]);
                    yesBut.setVisibility(View.VISIBLE);
                }  else if (currentTask.equals("retrieve_object")) {
                    dynamicText.setText(getString(R.string.squirtleRetr) + temp[1]);
                    yesBut.setVisibility(View.VISIBLE);
                } else if (currentTask.equals("deliver_object")) {
                    dynamicText.setText(getString(R.string.squirtleDeli) + temp[1]);
                    yesBut.setVisibility(View.VISIBLE);
                } else if (currentTask.equals("follow_person")) {
                    dynamicText.setText(getString(R.string.squirtleFollow)+ temp[1]);
                    yesBut.setVisibility(View.GONE);
                } else if (currentTask.equals("retrieve_message")) {
                    dynamicText.setText(getString(R.string.squirtleMsgRetrieve) + temp[1]);
                    yesBut.setVisibility(View.GONE);
                } else if (currentTask.equals("deliver_message")) {
                    dynamicText.setText(getString(R.string.squirtleMsgDeliver) + temp[1]);
                    yesBut.setVisibility(View.VISIBLE);
                }  else if (currentTask.equals("task_not_started")) {
                    dynamicText.setText(getString(R.string.squirtleWait) + temp[1]);
                    yesBut.setVisibility(View.GONE);
                } else {
                    dynamicText.setText("I can't decipher the weird code that they wrote!!!");
                    yesBut.setVisibility(View.GONE);
                }
            }
        });
    }

    @Override
    public void onPause() {
        super.onPause();
        //Pausing can be the end of an app if the device kills it or the user doesn't open it again
        //close all connections so resources are not wasted

        //Close BT socket to device
        try {
            btSocket.close();
        } catch (IOException e2) {
            Toast.makeText(getBaseContext(), "ERROR - Failed to close Bluetooth socket", Toast.LENGTH_SHORT).show();
        }
    }

    //takes the UUID and creates a comms socket
    private BluetoothSocket createBluetoothSocket(BluetoothDevice device) throws IOException {

        return device.createRfcommSocketToServiceRecord(MY_UUID);
    }

    //same as in device list activity
    private void checkBTState() {
        // Check device has Bluetooth and that it is turned on
        if (btAdapter == null) {
            Toast.makeText(getBaseContext(), "ERROR - Device does not support bluetooth", Toast.LENGTH_SHORT).show();
            finish();
        } else {
            if (btAdapter.isEnabled()) {
            } else {
                //Prompt user to turn on Bluetooth
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(enableBtIntent, 1);
            }
        }
    }

    // Method to send data
    private void sendData(String message) {
        byte[] msgBuffer = message.getBytes();

        try {
            //attempt to place data on the outstream to the BT device
            outStream.write(msgBuffer);
        } catch (IOException e) {
            //if the sending fails this is most likely because device is no longer there
            Toast.makeText(getBaseContext(), "ERROR - Device not found", Toast.LENGTH_SHORT).show();
            finish();
        }
    }

    // Button Functions: yes button
    public void buttonPress(View view)
    {
        sendData("button_pressed$");
    }

}
