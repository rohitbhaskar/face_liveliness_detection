package com.example.android.camera2video;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

import android.os.AsyncTask;
import android.util.Log;

import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;


public class HttpFileUpload extends AsyncTask<FileInputStream, Void, Void> implements Runnable{
    URL connectURL;
    File file;
    String responseString;
    String Title;
    String Description;
    byte[ ] dataToServer;
    FileInputStream fileInputStream = null;

    private final OkHttpClient client = new OkHttpClient();

    HttpFileUpload(String urlString, String vTitle, String vDesc, File videoFile){
        try{
            file = videoFile;
            connectURL = new URL(urlString);
            Title= vTitle;
            Description = vDesc;
        }catch(Exception ex){
            Log.i("HttpFileUpload","URL Malformatted");
        }
    }

    @Override
    protected Void doInBackground(FileInputStream...fStream) {
        fileInputStream = fStream[0];
        Sending();
        return null;
    }


    public void Sending(){
        try {
            RequestBody requestBody = new MultipartBody.Builder()
                    .setType(MultipartBody.FORM)
                    .addFormDataPart("video", file.getName(),
                            RequestBody.create(MediaType.parse("video/mp4"), file))
                    .addFormDataPart("motionType", "1")
                    .build();

            Request request = new Request.Builder()
                    .url(connectURL)
                    .post(requestBody).build();

//
            try (Response response = client.newCall(request).execute()) {
                if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

                System.out.println(response.body().string());
            }
//            return true;
        } catch (Exception ex) {
            // Handle the error
            Log.i("http post error", String.valueOf(ex));
        }
    }

    @Override
    public void run() {
        // TODO Auto-generated method stub
    }
}
