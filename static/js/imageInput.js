var startPath = "../img/training"
var namesDirectories = ["shirt men", "sportswear men", "trousers men", "t-shirt men", 
"dress business", "dress casual", "dress homemade", "dress solemn", "shirt women", "sportswear women", "trousers women", "t-shirt women"]

const nameFiles = [
['0 (4).jpg','0.png','1 (4).jpg','2 (3).jpg','3 (3).jpg','4 (2).jpg','4 (4).jpg','5 (2).jpg','7 (3).jpg','8 (2).jpg'], 
['00d6d20d74b446772e5090f1e18bea8f.jpg','0d6059010082727a59238494c76588c4.jpg','0q6ilubrom4pr0hf9scjdjwqqwotwmrg.jpg','1eacfdd728cefa9d5f258805b09bc813.jpg','1h2z7lf41pciqcu7cbhrz7vml4myoccx.jpg','2hoplx44gx30gi5uyeprmb8ceufhx5bl.png','4db494b3b4f719085a029ecde7344fa8.jpg','4e50e727e020ed1d91af7458be369e94.png','06f0261fbc967b49d2d368f469591f12.jpg','8bb0ccd57b5ff0fd5def5a9f449c4652.jpg'], 
['0 (2).jpg','t_image.jpg','1 (2).jpg','1 (3).jpg','2 (2).jpg','2.jpg','2.png','3 (2).jpg','3 (3).jpg','3 (4).jpg'],
['5.jpg','7.jpg','11.jpeg','18.jpeg','11478418_7279899_480.jpg','12074338_9753939_480.jpg','12147157_10105325_480.jpg','12559186_11995986_480.jpg','12965421_13582339_480.jpg','12687446_12520335_480.jpg'], 
['1 (3).jpg', '1 (4).jpg', '1 (4).jpg', '3 (2).jpg', '3.jpg', '4 (2).jpg', '4 (5).jpg', '4.jpg', '5 (2).jpg', '5 (3).jpg'],
['0 (2).jpg','1.jpg','3 (2).jpg','4.jpg','5 (2).jpg','5.jpg','6.jpg','7.png','8 (2).jpg','8.jpg'],
['0.png','7.png','8 (2).jpg','9 (2).jpg','12 (2).jpg','26.jpg','30 (2).jpg','30.jpg','38 (2).jpg','42.jpg'],
['1 (5).jpg','2 (2).jpg','2 (5).jpg','2.jpg','4 (2).jpg','5 (2).jpg','5 (4).jpg','6 (3).jpg','8 (5).jpg','9 (2).jpg'],
['0 (2).jpg','0 (4).jpg','0 (5).jpg','0.jpg','1.jpg','2 (2).jpg','2.png','5 (2).jpg','7 (2).jpg','7 (5).jpg'],
['7 (3).jpg','17 (7).jpg','26 (4).jpg','30 (2).jpg','33 (3).jpg','37 (2).jpg','44 (4).jpg','48 (4).jpg','49 (3).jpg','52 (2).jpg'],
['11640643_7697795_480.jpg','11772844_8406503_480.jpg','11812806_24428600_480.jpg','11880288_41822407_480.jpg','12647124_29992144_480.jpg','13013031_13747772_480.jpg','13375373_16144878_480.jpg','13490594_15885680_480.jpg','13570051_23002037_480.jpg','13570054_20843021_480.jpg'],
['1.jpg','2 (2).jpg','4.jpg','5.jpg','8.jpg','12.jpg','13.jpg','14.jpg','16.jpg','17.jpg']
]

var class_number = "0";
var file_name = "";
var arrayFullFiles = [];

function processFiles(files) {
  var file = files[0];

  let inputName = document.querySelector("#namefile");
  if (file.name !== "") {
    inputName.value = "Файл: " + file.name;
    file_name = file.name;
}

  var reader = new FileReader();

  reader.onload = function (e) {
    // Используем URL изображения для заполнения фона
	dropBox.style.backgroundImage = "url('" + e.target.result + "')";
  };
   
  // Начинаем считывать изображение
  reader.readAsDataURL(file);
}


function drop(e) {
  // Аннулируем это событие для всех других
  e.stopPropagation();
  e.preventDefault();
 
  // Получаем перемещенные файлы
  var data = e.dataTransfer;
  var files = data.files;

  // Передаем полученный файл функции для обработки файлов
  processFiles(files);
}


function ignoreDrag(e) {
  // Обеспечиваем, чтобы никто другой не получил это событие, 
  // т.к. мы выполняем операцию перетаскивания
  e.stopPropagation();
  e.preventDefault();
}


var dropBox;

window.onload = function() {
  dropBox = document.getElementById("dropBox");
  dropBox.ondragenter = ignoreDrag;
  dropBox.ondragover = ignoreDrag;
  dropBox.ondrop = drop;
  
}


document.onpaste = function(pasteEvent) {
  // рассмотрим первый элемент (можно легко расширить для нескольких элементов)
    var item = pasteEvent.clipboardData.items[0];
 
    if (item.type.indexOf("image") === 0)
    {
        var blob = item.getAsFile();
 
        var reader = new FileReader();
        reader.onload = function(event) {
            document.getElementById("dropBox").style.backgroundImage = "url('" + event.target.result + "')";
        };
 
        reader.readAsDataURL(blob);
    }
}


function input_click( event)
{
  event.stopPropagation();
  return false;
}

function btn_click(btnEle, event)
{
  if (class_number != 0)
  {
    const dropDowns = document.querySelectorAll('.btn-class');
    dropDowns.forEach(item => item.classList.remove('activated'));
      
  }

  class_number = btnEle.name;

  btnEle.classList.add("activated");

  getFiles(classDirectory(class_number));

    //console.log(class_number + " " + file_name);
}

function classDirectory (numberClass) {
    path = startPath + "/" + namesDirectories[numberClass-1];
    return path;
  }

function getFiles (path) {
  console.log(path);

  const images = [];
  for (i=0; i<10; i++)
  {
    images.push(startPath+'/'+namesDirectories[class_number-1]+'/'+nameFiles[class_number-1][i]);
  }
  //console.log(images);

  const container = document.getElementById('image-container');
  container.innerHTML = "";
  images.forEach(image => {
      const img = document.createElement('img');
      img.src = image;
      container.appendChild(img);
  })

}

function outputFiles () {
  for (var i=0; i<10; i++) {
    console.log(namesDirectories[i]);
  }
  console.log(namesDirectories.length);
}

function click_category(btnCategory, event) {
  if (btnCategory.name == "man") {
      document.getElementById('moda_woman').style.display = "none";
      document.getElementById("moda_man").style.display = "block";
      
  }
  else {
      document.getElementById('moda_man').style.display = "none";
      document.getElementById('moda_woman').style.display = "block";
      
  }
   const dropDowns = document.querySelectorAll('.btn-class');
    dropDowns.forEach(item => item.classList.remove('activated'));
}


function onChange_man(x, event) {
  var e = document.getElementById("moda_man");
  class_number = e.value;
  getFiles(classDirectory(class_number));
  //console.log(class_number);
}

function onChange_woman(x, event) {
  var e = document.getElementById("moda_woman");
  class_number = e.value;
  getFiles(classDirectory(class_number));
  //console.log(class_number);
}
