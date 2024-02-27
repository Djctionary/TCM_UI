// Ensure the script runs after the document is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Get the input element by ID
    var inputElement = document.getElementById('myInput');

    ID = localStorage.getItem('myInput');

    inputElement.value = ID;

    var boxText1 = document.getElementById('boxText1');
    var boxText2 = document.getElementById('boxText2');
    var boxText3 = document.getElementById('boxText3');
    var boxText4 = document.getElementById('boxText4');

    Box1 = localStorage.getItem('boxText1');
    Box2 = localStorage.getItem('boxText2');
    Box3 = localStorage.getItem('boxText3');
    Box4 = localStorage.getItem('boxText4');

    boxText1.value = Box1;
    boxText2.value = Box2;
    boxText3.value = Box3;
    boxText4.value = Box4;
});

function focusOnInput() {
    // 获取输入框元素
    var inputElement = document.getElementById("myInput");

    // 将焦点设置到输入框上
    inputElement.focus();
}

var bar = document.getElementById("bar");

function updateProgress(i) {
    bar.style.setProperty("--progress", i * 10 + "%");
}

for (var i = 1; i <= 10; i++) {
    setTimeout(function () {
        updateProgress(i);
    }, i * 1000);
}


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

    localStorage.setItem('myInput', (inputValue));

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

    localStorage.setItem('myInput', (inputValue));

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

    localStorage.setItem('myInput', (inputValue));

    // 触发超链接跳转
    window.location.href = "record.html?source=" + inputValue + "_步态记录";
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

    localStorage.setItem('myInput', (inputValue));

    // 触发超链接跳转
    window.location.href = "record.html?source=" + inputValue + "_患者自述";
}

// 为患者自述元素添加点击事件监听器
faceRecognition.addEventListener("click", handleClick4);




var boxText1 = document.getElementById('boxText1');
var boxText2 = document.getElementById('boxText2');
var boxText3 = document.getElementById('boxText3');
var boxText4 = document.getElementById('boxText4');

function inputBoxStorage(event) {

    var name = event.id
    // console.log(name);

    var content = event.value;
    // console.log(content);
    
    localStorage.setItem(name, content);
}


boxText1.addEventListener('change', (event) => inputBoxStorage(boxText1))
boxText2.addEventListener('change', (event) => inputBoxStorage(boxText2))
boxText3.addEventListener('change', (event) => inputBoxStorage(boxText3))
boxText4.addEventListener('change', (event) => inputBoxStorage(boxText4))
