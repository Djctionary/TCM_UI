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
function handleClick() {
    // 移除可能已有的 animate 类
    faceRecognition.classList.remove("animate");

    // 设置鼠标样式为手型   
    faceRecognition.style.cursor = "pointer";

    // 触发超链接跳转
    window.location.href = "record.html?source=面部识别";
}

// 为面部识别元素添加点击事件监听器
faceRecognition.addEventListener("click", handleClick);