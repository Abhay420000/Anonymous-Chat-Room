var my_name;
var my_id;
var room_status = 1;
var room_code;
var chatSocket;
var current_room_size;
var max_room_size;

const other_person_cb_1 = `
<div class="row ps-1 msg-pack">

  <div style="font-size: 12px;">`;
    //TIME AND PERSON
const other_person_cb_2 = `
  </div>

  <div class="d-flex justify-content-start">
    <div class = "px-2 msg" style="overflow-x:hidden; max-width:fit-content; background-color: white; white-space: pre-wrap; word-wrap: break-word;">`;
    //CHAT MSGs
const other_person_cb_3 = `
    </div>

    <div style="width: 20%;">
      &nbsp;
    </div>
  </div>
</div>
<br>`;

const me_cb_1 = `
<div class="row pe-1 msg-pack">
  <div class="d-flex justify-content-end" style="font-size: 12px;">`;
  //TIME AND PERSON
const me_cb_2 = `
  </div>
  <div class="d-flex justify-content-end">
    <div class="d-flex justify-content-end" style="width: 20%;">
      &nbsp;
    </div>
    <div class = "px-2 msg" style="word-wrap: break-word; overflow-x:hidden; max-width:fit-content; background-color: lightgreen; white-space: pre-wrap;">`;
    //CHAT MSG
const me_cb_3 = `
    </div>
  </div>
</div>
<br>`;

const lj_msg_1 = `<center>
<div class="d-flex justify-content-center w-75 msg" style="background-color: white;">`;
//Left or Join Message
const lj_msg_2 = `</div>
</center>
<br>`;

function display_toc(){
  //Used to display terms of conditions page
  for (i=0; i<document.body.children.length; i++){
    document.body.children[i].style.display = "none";
  }
  $("#toc")[0].style.display = "block";
  document.body.style="overflow: hidden;"
}

function display_pp(){
  //Used to display privacy policy
  for (i=0; i<document.body.children.length; i++){
    document.body.children[i].style.display = "none";
  }
  $("#pp")[0].style.display = "block";
  document.body.style="overflow: hidden;"
}

function back_home(from){
  if (from == "chat"){
    s_chat("leave_room");
  }
  for (i=0; i<document.body.children.length; i++){
    document.body.children[i].style.display = "none";
  }
  $("#home")[0].style.display = "block";



  //Backgroud Image chat.png
  document.body.style="overflow: hidden; background-image: url(static/chat.png); background-repeat: no-repeat; background-size: cover;  background-size: 100% 100%;";
}

function s_chat(args){
  //Accept terms and conditions before creating room
  if ($("#accept")[0].checked == false){
    alert("Please accept Terms and Conditions.");
    return;
  }

  clean_msg();

  for (i=0; i<document.body.children.length; i++){
    document.body.children[i].style.display = "none";
  }

  $("#loading")[0].style.display = "block";//start loading

  //Client Request- Create Room
  if (args == "create_room"){
    data = {
      'name': $('.inpele')[0].value, 
      'language': $('.inpele')[1].value, 
      'country': $('.inpele')[2].value, 
      'max_room_size': $('.inpele')[3].value,
      'action': "create room",
    }

    max_room_size = $('.inpele')[3].value;

  } else if (args == "join_room"){
    //Client Request- Join Room
    data = {
      'name': $('#yname')[0].value,
      'room_code': $('#rid')[0].value,
      'action': 'join room'
    }
  } else if (args == "leave_room"){
    `
    data = {
      "id": my_id,
      "room_code":  room_code,
      "action": "leave room"
    }
    `
    //Closeing websocket
    chatSocket.close()
    return;

  } else{
    alert("Unknown Error Occured!");
    return;
  }

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

  var data = JSON.stringify(data);                                                     
  xhttp.send(data);

  xhttp.onload = function() {
    res = JSON.parse(xhttp.responseText);
    
    console.log(res);
    console.log(args);
    
    $("#loading")[0].style.display = "none";//stop loading
    
    if (args == "create_room") {

      //Display chatting page
      $("#chat")[0].style.display = "block";
      $("#room_code")[0].innerHTML = res["room_code"];
      document.body.style="overflow: hidden;"

      //Adjust Variable Names
      my_name = res["name"]
      my_id = res["id"]
      room_code = res["room_code"]

      //Start Chat
      start_chatting();
      
    } else if (args == "join_room"){

      if (res["status"] == "failed"){
        
        //Display error message
        $("#msg_title")[0].innerHTML = "Error!";
        $("#msg_body")[0].innerHTML = res["msg"];
        $('#dis_msg').modal('show');

        //Display home page again
        $("#home")[0].style.display = "block";
        document.body.style="overflow: hidden; background-image: url(static/chat.png); background-repeat: no-repeat; background-size: cover;  background-size: 100% 100%;";
        return;

      } else if (res["status"] == "success"){
        
        //Display chatting page
        $("#chat")[0].style.display = "block";
        $("#room_code")[0].innerHTML = $('#rid')[0].value;
        document.body.style="overflow: hidden;"

        //Adjust Variable Names
        my_name = res["name"]
        my_id = res["id"]
        room_code = res["room_code"]

        //Start Chat
        start_chatting();
      }
    }
  }
}

function start_chatting() {
  //console.log(1);
  chatSocket = new WebSocket(
      'ws://'
      + window.location.host
      + '/ws/chat/'
      + room_code
      + '/'
      + my_id
      + '/'
  );
  
  chatSocket.onmessage = function (msg) {
      data = JSON.parse(msg.data);
      //console.log(data);

      if (data["type"] == "chat_message"){
        //append chat_messages to chat room
        append_msg(data["msg"], get_ctime(), data["name"]);
      } else if(data["type"] == "leave_message"){
        //append leave_messages to chat room
        lj_msg(data["name"], "leave");
        current_room_size -= 1;
        $("#upd_mem")[0].innerHTML = `<i class="fa fa-circle" aria-hidden="true" style="color: green;"></i> `+current_room_size+`/`+max_room_size;
      }
      else if(data["type"] == "join_message"){
        //append join_messages to chat room
        lj_msg(data["name"], "join");

        //Update member count data
        current_room_size = data["current_room_size"];
        max_room_size = data["max_room_size"];
        $("#upd_mem")[0].innerHTML = `<i class="fa fa-circle" aria-hidden="true" style="color: green;"></i> `+current_room_size+`/`+max_room_size;
      }
      else{
        console.log("error!");
      }
  };
}

function clean_msg(){
  //Cleaning message box
  $("#fill_msg")[0].innerHTML = ""
}

function get_ctime(){
  //Return the current time
  const d = new Date();
  hr = d.getHours();
  min = d.getMinutes();

  single_chr = [0,1,2,3,4,5,6,7,8,9];

  if (hr in single_chr && !(min in single_chr)){
    return "0"+hr+":"+min;
  }
  else if ((hr in single_chr) && (min in single_chr)){
    return "0"+hr+":0"+min;
  }
  else if (!(hr in single_chr) && (min in single_chr)){
    return hr+":0"+min;
  }
  else{
    return hr+":"+min;
  }
}

function lj_msg(name, status) {
  if (status == "join"){
    $("#fill_msg").append(lj_msg_1+name+" joined the room!"+lj_msg_2);
  } else{
    $("#fill_msg").append(lj_msg_1+name+" left the room!"+lj_msg_2);
  }
}

function append_msg(msg, time, person){
  /*
  Used to append message in message box
  person - my_name OR other Person's Name
  */
  msg = msg.trim()
  if (msg==""){
    return;
  }
  if (my_name == person){
    $("#fill_msg").append(me_cb_1+time+" "+person+me_cb_2+msg+me_cb_3);                                                   
  }
  else{
    $("#fill_msg").append(other_person_cb_1+time+" "+person+other_person_cb_2+msg+other_person_cb_3);                                                   
  }
}

function my_msg(){
  //Used to append our msg in msg box
  let msg = $("#msg_to_send")[0].value;
  append_msg(msg, get_ctime(), my_name);
  $("#msg_to_send")[0].value = "";

  //Sending data to server
  data = {"name": my_name, "msg": msg, "uid": my_id,}
  chatSocket.send(JSON.stringify(data));
}

function getCaret(el) { 
  if (el.selectionStart){
    return el.selectionStart; 
  }
  else if (document.selection){
    el.focus();
    var r = document.selection.createRange(); 
    if (r == null){
      return 0;
    }
    var re = el.createTextRange(), rc = re.duplicate();
    re.moveToBookmark(r.getBookmark());
    rc.setEndPoint('EndToStart', re);
    return rc.text.length;
  }  
  
  return 0; 
}

function epkey(event){
  if (event.keyCode == 13) {
      var content = this.value;  
      var caret = getCaret(this);
      if(event.shiftKey){
          this.value = content.substring(0, caret - 1) + "\n" + content.substring(caret, content.length);
          event.stopPropagation();
      } else {
          my_msg();
      }
  }
}

document.getElementById("msg_to_send").addEventListener("keyup",epkey);


function check_room(room_code, auto_join, name=null){
  /*
    Used to check if room code label is filled or empty
    In "Already have room code?"
  */
  if (room_code == ""){
    alert("Room Code is required!");
    return;
  }
  console.log(room_code, auto_join, name);
  $('#rcode').modal('hide');
  s_chat("join_room");
}

function change_status(me_oth,){
  /*
  Available for only admins to alter
  Just to preview for other members.
  
  me_oth = 1 -> I have changed room status
  me_oth = 0 -> Some Admin have changed room status
  */
  if (is_admin == false && me_oth == 1){
    return
  }

  if (room_status == 1){
    $("#room_status")[0].className = "btn btn-danger h-75 w-100";
    $("#room_status")[0].textContent = "Close";
    room_status = 0
  }
  else{
    $("#room_status")[0].className = "btn btn-success h-75 w-100";
    $("#room_status")[0].textContent = "Open";
    room_status = 1
  }
}

function sendREQ(data){
  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "", true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  
  var data = JSON.stringify(data);                                                     
  xhttp.send(data);

  xhttp.onload = function() {
    res = JSON.parse(xhttp.responseText);
    console.log(res);
  }

}

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }