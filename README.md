### DSCI6007 Sparkify Lab 1

### **Task** 

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
The analytics team is particularly interested in understanding what songs users are listening to. 
Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON 
metadata on the songs in their app. The dataset can be found in the `data` directory.

Create a Python web application with Flask to display the top 10 (i.e., most frequently played) Songs and the top 10 Artists for each week on a web page. Host the web 
application on an AWS EC2 Instance (Ubuntu AMI).

### **Solution**

- The `create_db.py` script creates the database with five collection objects corresponding to five weeks in the given dataset on MongoDB.
- `app.py` is the flask web app that generates an HTML file `./templates/top.html` that displayes the top 10 songs and artists. 


#### AWS EC2 Configuration

- [MongoDB Installation: Ubuntu](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)
- Allowed inbound traffics in ports HTTP (80), SSH (22), HTTPS (443) and 27017 in EC2 Security Groups.
- SSH into the instance. Install a Python virtual environment.
```
sudo apt-get update
sudo apt-get install python3-venv
```
- Create a directory for the project
```
mkdir sparkify1
cd sparkify1
```
- Activate Python venv 
```
python3 -m venv venv
source venv/bin/activate
```
- Install requirements
```
pip install -r requirements.txt
```
- Run Gunicorn
```
gunicorn -b 0.0.0.0:8000 app:app
``` 
Ctrl+C to exit
- Create *app.service* in the `/etc/systemd/system` directory so that Gunicorn restarts with every instance reboot.
```
sudo systemctl daemon-reload
sudo systemctl start app
sudo systemctl enable app
```
- Check if `app.py` is running
```
curl localhost:8000
```
- Install Nginx webserver 
```
sudo apt-get nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```
- Add a proxy_pass following [this tutotial](https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7#:~:text=Edit%20the%20default%20file%20in%20the%20sites%2Davailable%20folder.)
```
sudo systemctl restart nginx
```

Now the Flask app is running on EC2.
