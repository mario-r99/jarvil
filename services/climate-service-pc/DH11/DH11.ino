//DHT11 datapull by Arduino
//Author: Samson Yang
//Date: 10/26/2019
//It without using any libaray.  This is a very not effective way to pull data out of DHT11
//But, after familiar with how DHT11 and DHT22 work, the same experience can be applied to other device.
//read datasheet from
// http://www.produktinfo.conrad.com/datenblaetter/1400000-1499999/001405544-da-01-en-TEMP_UND_FEUCHTESENSOR_DHT11.pdf
//
int L=600;                        //Use 600 data point to pull data into matrix 
boolean data[1000];               //Need to be more then above L
boolean result[100];              //Need to be more then 40 
int resultcount=0;                //End result shoudl be 39.
int data_pin=2;                   //Set the data pin location
int extract_data_threadhold = 8;  //This threadhold between 0 or 1. It is the counts of high status between low voltage.
int DHT_type=11;                  //11 means DHT11, 22 means DHT22.  It will only be used at the end of data caculation

// Above setting is only good for Arduino nano.
// For faster board, you will need to change "extract_data_threadhold" and L.

void setup() {
  Serial.begin(9600);  
}

void Get_Data(){
  for (int i = 0; i <= L; i++) {
    data[i]=digitalRead(data_pin);
    delayMicroseconds(5);
    }
}

void Display_Result(){
  for (int i = 0; i <= L; i++) {
    Serial.println(data[i]);
    data[i]=0;
    }
  Serial.println();
  delay(5000);
}

void loop(){
  readDHT();
  delay(1000);  
}
void readDHT() {
  // Go into high impedence state to let pull-up raise data line level and
  // start the reading process.  Pull from HIGH to LOW to tell DHT11 prepare sending dada out
  pinMode(data_pin, OUTPUT);
  //Pull up the data pin prepare for the next step
  digitalWrite(data_pin, HIGH);delay(250);  
  // First set data line low for 20 milliseconds to trigger DHT11 to start generate result.
  // Page 5 in datasheet, it needs >18ms.  
  digitalWrite(data_pin, LOW);delay(20); 

  // End the start signal by setting data line high for 40 microseconds.
  digitalWrite(data_pin, HIGH);
  delayMicroseconds(40);

  // Now start reading the data line to get the value from the DHT sensor.
  pinMode(data_pin, INPUT_PULLUP);  
  delayMicroseconds(50);  // Delay a bit to let sensor pull data line low, and wait till low before get data.   
  Get_Data();
  //Display_Result();  //You can use Serial Plot to see the data like oscolscope
  extract_data();  //Extract data and show end reult.
}

void extract_data(){
  int high=0;
  resultcount=0;
  
  for (int i = 0; i< L-1;i++){
    if ((data[i]==true)){high++;}
    if ((data[i]==false)){
      if (high>0){if(high > extract_data_threadhold){result[resultcount]=true;high=0;resultcount++;}}
      if (high>0){if(high < extract_data_threadhold){result[resultcount]=false;high=0;resultcount++;}}
      }
    }
  
  //for (int j = 0; j<= resultcount;j++){
  for (int j = 0; j< 40;j++){
    result[j]=result[j+1];
    Serial.print(result[j]);
    if (((j+1)/8.0)==int((j+1)/8.0)){Serial.print(" ");}//Add a space every 8 bits
    }  
  Serial.println();   
  //Prepare 2^i.  Arduino IDE do not understand ^ operant 
  double powerof2[16];
  powerof2[0]=1;
  for (int i=1;i<16;i++){
    powerof2[i]=1;
    for (int j=0;j<i;j++){
      powerof2[i]=powerof2[i]*2;  
    }
  }


  //Caculate for DHT11
  if (DHT_type==11){ 
    int startpoint=0;
    double HR=0, TM=0;  
    //Extract HR, temperature, and verify code
    for (int i=0;i<8;i++){
      HR=HR+powerof2[7-i]*(result[i]*1.0);
      TM=TM+powerof2[7-i]*(result[16+i]*1.0);
      //Serial.print("Debug:");Serial.print(" i=");Serial.print(i);Serial.print(" powerof2[15-i]=");Serial.print(powerof2[15-i]);Serial.print(", result[i]=");Serial.print(result[i]);Serial.print(" HR=");Serial.print(HR);Serial.print(" TM=");Serial.print(TM);Serial.println();
      //delay(500);
    }
    
    //Check SUM with 5th byte, ignore overflow
    int VR1=0,VR2=0,VR3=0,VR4=0,VRR=0,VR=0;
    for (int i=0;i<8;i++){
      VR1=VR1+powerof2[7-i]*(result[i]*1.0);    //1st byte
      VR2=VR2+powerof2[7-i]*(result[i+8]*1.0);  //2nd byte
      VR3=VR3+powerof2[7-i]*(result[i+16]*1.0); //3rd byte
      VR4=VR4+powerof2[7-i]*(result[i+24]*1.0); //4th byte
      VR=VR+powerof2[7-i]*(result[i+32]*1.0);   //VR byte      
    }
    VRR=VR1+VR2+VR3+VR4;
    if (VRR>=256)VRR=VRR-256;  //Remove overflow 
    HR=HR;
    TM=TM;
    
    Serial.print("DHT11, HR = ");Serial.print(HR,0);Serial.print("%, Temperature = ");Serial.print(TM,0);Serial.print("C.  Data status is ");
    if ((VRR-VR)==0){Serial.println("verified!");} else {Serial.println("NOT verified!");Serial.println();}    
  }
  //Caculate for DHT22
  if (DHT_type==22){ 
    int startpoint=0;
    double HR=0, TM=0;  
    //Extract HR, temperature, and verify code
    for (int i=0;i<16;i++){
      HR=HR+powerof2[15-i]*(result[i]*1.0);
      TM=TM+powerof2[15-i]*(result[16+i]*1.0);
      //Serial.print("Debug:");Serial.print(" i=");Serial.print(i);Serial.print(" powerof2[15-i]=");Serial.print(powerof2[15-i]);Serial.print(", result[i]=");Serial.print(result[i]);Serial.print(" HR=");Serial.print(HR);Serial.print(" TM=");Serial.print(TM);Serial.println();
      //delay(500);
    }
    
    //Check SUM with 5th byte, ignore overflow
    int VR1=0,VR2=0,VR3=0,VR4=0,VRR=0,VR=0;
    for (int i=0;i<8;i++){
      VR1=VR1+powerof2[7-i]*(result[i]*1.0);    //1st byte
      VR2=VR2+powerof2[7-i]*(result[i+8]*1.0);  //2nd byte
      VR3=VR3+powerof2[7-i]*(result[i+16]*1.0); //3rd byte
      VR4=VR4+powerof2[7-i]*(result[i+24]*1.0); //4th byte
      VR=VR+powerof2[7-i]*(result[i+32]*1.0);   //VR byte      
    }
    VRR=VR1+VR2+VR3+VR4;
    if (VRR>=256)VRR=VRR-256;  //Remove overflow 
    HR=HR/10.0;
    TM=TM/10.0;
    
    Serial.print("DHT22, HR = ");Serial.print(HR,1);Serial.print("%, Temperature = ");Serial.print(TM,1);Serial.print("C.  Data status is ");
    if ((VRR-VR)==0){Serial.println("verified!");} else {Serial.println("NOT verified!");Serial.println();}    
  }
}
