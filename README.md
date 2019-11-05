# RFM-Ideorum

data: incluye archivo retail-rfm.py que ejecuta cálculos de scor RFM y agregraciones.

web: app web desarrollada con react

step to run web app:

Install the app dependencies by running the following command in the command line inside the folder root where you have unzipped the theme package archive.


    npm install
                                                        
After npm finishes installing the modules from package.json you can go ahead and start the application. To do so, run the command below.

You can also use yarn to install dependencies instead of npm.


    npm run start
                                                        
After the comand finished, you should see a Compiled successfully! message in your terminal window. Also, a web server service will be started so you can view your app in the browser: http://localhost:3000

### Production Build

To create a production optimised build run the command below:


    npm run build
                                                        
This created another folder in the root of your project named build. You'll have an option to start a local web server to view your newly created production build.


    serve -s build -l 4000
                                                        
This will start a local web server on port 4000, on which the production folder (/build/) will be available in your browser.
