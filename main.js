// Ensure the script runs after the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the input element by ID
    var inputElement = document.getElementById('myInput');

    ID = localStorage.getItem('myInput');
    
    inputElement.value = ID;
});

var bar = document.getElementById("bar");

function updateProgress(i) {
    bar.style.setProperty("--progress", i * 10 + "%");
}

for (var i = 1; i <= 10; i++) {
    setTimeout(function () {
        updateProgress(i);
    }, i * 1000);
}

// var xhr = new XMLHttpRequest();
// xhr.open('HEAD',"result",false);
// xhr.send();
// if(xhr.status == 200) {
//     alert("存在")
// }
// else {
//     alert("不存在")
// }
// prompt("请创建文件夹");

// const fs = require('fs');
// fs.mkdir('hello');



// 获取面部识别元素
var faceRecognition = document.getElementById("面部识别");

// 点击事件处理函数
function handleClick1() {
    // 移除可能已有的 animate 类
    faceRecognition.classList.remove("animate");

    // 设置鼠标样式为手型   
    faceRecognition.style.cursor = "pointer";

    var inputElement = document.getElementById('myInput');
    
    var inputValue = inputElement.value;
    
    localStorage.setItem('myInput',(inputValue));
    
    // 触发超链接跳转
    window.location.href = "record.html?source=" + inputValue + "_面部识别";
}

// 为面部识别元素添加点击事件监听器
faceRecognition.addEventListener("click", handleClick1);


// 获取舌相抓取元素
var faceRecognition = document.getElementById("舌相抓取");

// 点击事件处理函数
function handleClick2() {
    // 移除可能已有的 animate 类
    faceRecognition.classList.remove("animate");    

    // 设置鼠标样式为手型   
    faceRecognition.style.cursor = "pointer";

    var inputElement = document.getElementById('myInput');
    
    var inputValue = inputElement.value;
    
    localStorage.setItem('myInput',(inputValue));
    
    // 触发超链接跳转
    window.location.href = "record.html?source=" + inputValue + "_舌相抓取";
}

// 为舌相抓取元素添加点击事件监听器
faceRecognition.addEventListener("click", handleClick2);


// 获取步态记录元素
var faceRecognition = document.getElementById("步态记录");

// 点击事件处理函数
function handleClick3() {
    // 移除可能已有的 animate 类
    faceRecognition.classList.remove("animate");

    // 设置鼠标样式为手型   
    faceRecognition.style.cursor = "pointer";

    var inputElement = document.getElementById('myInput');
    
    var inputValue = inputElement.value;
    
    localStorage.setItem('myInput',(inputValue));
    
    // 触发超链接跳转
    window.location.href = "record.html?source=" + inputValue +"_步态记录";
}

// 为步态记录元素添加点击事件监听器
faceRecognition.addEventListener("click", handleClick3);


// 获取患者自述元素
var faceRecognition = document.getElementById("患者自述");

// 点击事件处理函数
function handleClick4() {
    // 移除可能已有的 animate 类
    faceRecognition.classList.remove("animate");

    // 设置鼠标样式为手型   
    faceRecognition.style.cursor = "pointer";

    var inputElement = document.getElementById('myInput');
    
    var inputValue = inputElement.value;
    
    localStorage.setItem('myInput',(inputValue));
    
    // 触发超链接跳转
    window.location.href = "record.html?source=" + inputValue + "_患者自述";
}

// 为患者自述元素添加点击事件监听器
faceRecognition.addEventListener("click", handleClick4);
