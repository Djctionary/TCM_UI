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

document.getElementById('文字转录').addEventListener('click', function() {
        // 发送 POST 请求到 Flask 服务器的 /run_python_script 路由
        alert('开始进行文字转录, 请点击 确定 后等待十秒到一分钟');
        fetch('/run_python_script', { method: 'POST' })
            .then(response => response.text())
            .then(result => {
                console.log(result);
                // 处理成功或错误的情况
                alert(result === 'Success' ? '文字转录成功, 正在生成诊断报告' : '文字转录失败');
                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function() {
                    if (xhr.readyState == 4 && xhr.status == 200) {
                        document.getElementById('Text').innerText = xhr.responseText;
                    }
                };
                xhr.open('GET', '/get_text', true);
                xhr.send();

                // 获取 <img> 元素
                var imageElement = document.getElementById('可视化图片');

                // 更新 <img> 元素的 src 属性
                imageElement.src = "static/visual_wav.jpg";

                // 显示图片
                document.getElementById('可视化图片').style.display = 'block';

            })
            .catch(error => {
                console.error('Error:', error);
                alert('发生错误，请检查控制台');
            });
});

// 打开放大图模态框
function openModal(imageSrc) {
    document.getElementById('myModal').style.display = 'flex';
    document.getElementById('modalImg').src = imageSrc;
}

// 关闭放大图模态框
document.getElementById('myModal').addEventListener('click', function() {
    this.style.display = 'none';
});

document.getElementById('保存').addEventListener('click', function() {
    alert('保存成功，请到output/Result文件夹下查看');

    var id = document.getElementById('myInput').value;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.open('POST', '/create_folder', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ 'id': id }));
});
