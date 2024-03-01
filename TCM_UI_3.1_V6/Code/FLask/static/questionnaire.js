function download() {
   if(check()==false)
   {
      alert("请填写所有问题");
      return false;
   }
  // 创建一个空字符串来存储答案
  let answersString = '';

  // 遍历表单中的所有输入元素
  var inputs = document.getElementsByTagName('input');

  for (var i = 0; i < inputs.length; i++) {
   if (inputs[i].type === 'text')
   {
        if(inputs[i].value.trim() != '')
            answersString += `${inputs[i].name}: ${inputs[i].value}\n`;
   }
   else if(inputs[i].type === 'radio')
   {
        if(inputs[i].checked)
            answersString += `${inputs[i].name}: ${inputs[i].value}\n`;
   }
   else if(inputs[i].type === 'checkbox')
   {
        if(inputs[i].checked)
            answersString += `${inputs[i].name}: ${inputs[i].value}\n`;
   }
  }

  // 创建一个新的 Blob 对象，用于保存数据
  const blob = new Blob([answersString], { type: 'text/plain' });
  var title = document.title;
  var name = document.getElementById('name');
  // 创建一个下载链接
  const downloadLink = document.createElement('a');
  downloadLink.href = URL.createObjectURL(blob);

  downloadLink.download = name.querySelector('input').value + '的' + title + '.txt';

  // 为了安全起见，我们将在文档中隐藏这个链接，然后通过触发点击事件来下载文件
  document.body.appendChild(downloadLink);
  downloadLink.click();

  // 清理内存，移除下载链接
  document.body.removeChild(downloadLink);
  URL.revokeObjectURL(blob);
}


function check() {
    var inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type == 'text') {
            if (inputs[i].value.trim() === '') {
                //alert('Text input at index ' + i + ' is empty');
                return false; // 如果任何一个输入框未填写，返回false
            }
        }
        else if (inputs[i].type == 'radio') {
            var radioGroupName = inputs[i].name;
            var isChecked = false;
            for (var j = 0; j < inputs.length; j++) {
                if (inputs[j].type == 'radio' && inputs[j].name === radioGroupName) {
                    if (inputs[j].checked) {
                        isChecked = true;
                        break;
                    }
                }
            }
            if (!isChecked) {
                //alert('Radio button with name ' + radioGroupName + ' is not checked');
                return false; // 如果同名的选项中没有至少一个被选中，返回false
            }
        }
        else if (inputs[i].type == 'checkbox') {
            var radioGroupName = inputs[i].name;
            var isChecked = false;
            for (var j = 0; j < inputs.length; j++) {
                if (inputs[j].type == 'checkbox' && inputs[j].name === radioGroupName) {
                    if (inputs[j].checked) {
                        isChecked = true;
                        break;
                    }
                }
            }
            if (!isChecked) {
                //alert('Radio button with name ' + radioGroupName + ' is not checked');
                return false; // 如果同名的选项中没有至少一个被选中，返回false
            }
        }

    }
    return true; // 所有输入框和单选按钮都已填写或选中，返回true
}

document.getElementById('btn').addEventListener('click', function() {
    if(check()==true)
    {
        // 设置要跳转的URL
        window.location.href = 'thanks.html';
    }
});