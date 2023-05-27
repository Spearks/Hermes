

var iframe = document.getElementsByTagName('iframe')[0];
iframe.addEventListener("load", function() {
		/* the JS equivalent of the answer
     *
     * var node = document.createElement('style');
     * node.appendChild(document.createTextNode('body { background: #fff; }'));
     * window.frames[0].document.head.appendChild(node);
     */
    
    // the cleaner and simpler way
    window.frames[0].document.getElementsByClassName("panel-title")[0].style.display = "none";
});


function addchannel() {
    // Get the target div element
    var targetDiv = document.querySelector('.parentch');

    // Create a new div element
    var div = document.createElement('div');
    div.className = 'chview picker item';

    // Create a form element
    var form = document.createElement('form');
    form.action = 'excel';

    // Create the first input element
    var input1 = document.createElement('input');
    input1.className = 'form input';
    input1.type = 'datetime-local';
    input1.value = '2023-04-30T00:00';
    input1.id = 'time';
    input1.name = 'time';

    // Create the box-icon element
    var boxIcon = document.createElement('box-icon');
    boxIcon.className = 'form alt';
    boxIcon.setAttribute('name', 'tag-alt');
    boxIcon.setAttribute('type', 'solid');
    boxIcon.setAttribute('color', '#ffffff');

    // Create the second input element
    var input2 = document.createElement('input');
    input2.className = 'form input';
    input2.type = 'datetime-local';
    input2.value = '2023-04-30T00:00';
    input2.id = 'time';
    input2.name = 'time-f';

    // Create the third input element
    var input3 = document.createElement('input');
    input3.className = 'form input points';
    input3.type = 'number';
    input3.id = 'pontos';
    input3.name = 'pmin';

    // Create the label element
    var label = document.createElement('label');
    label.className = 'form input points text';
    label.setAttribute('for', 'pmin');
    label.textContent = 'P/min';

    // Append the elements to their respective parent elements
    form.appendChild(input1);
    form.appendChild(boxIcon);
    form.appendChild(input2);
    form.appendChild(input3);
    form.appendChild(label);

    div.appendChild(form);

    // Append the new div to the target div
    targetDiv.appendChild(div);

    var parentDiv = document.querySelector('.parentch');
    // Append the div to the body of the document

    var elementToDelete = document.querySelector('.plus');
    if (elementToDelete) {
      // Get the parent node of the element
      var parentElement = elementToDelete.parentNode;
    
      // Remove the element from its parent node
      parentElement.removeChild(elementToDelete);
    }

    var elementToDelete = document.querySelector('.report');
    if (elementToDelete) {
      // Get the parent node of the element
      var parentElement = elementToDelete.parentNode;
    
      // Remove the element from its parent node
      parentElement.removeChild(elementToDelete);
    }

    var svgElement = document.createElement('box-icon');
    svgElement.setAttribute('name', 'plus-circle');
    svgElement.setAttribute('class', 'plus');
    svgElement.setAttribute('onclick', 'addchannel();');
    svgElement.setAttribute('rotate', '90');
    svgElement.setAttribute('color', '#ffffff');

    // Create the parent <p> element
    var pElement = document.createElement('p');
    pElement.setAttribute('class', 'report');
    pElement.setAttribute('onclick', 'apiExportCall()');

    // Create the <a> element
    var aElement = document.createElement('a');
    aElement.textContent = 'Baixar';

    // Create the <box-icon> element
    var boxIconElement = document.createElement('box-icon');
    boxIconElement.setAttribute('name', 'down-arrow-circle');
    boxIconElement.setAttribute('class', 'down');
    boxIconElement.setAttribute('color', '#ffffff');

    // Append the <a> element to the parent <p> element
    pElement.appendChild(aElement);

    // Append the <box-icon> element to the parent <p> element
    pElement.appendChild(boxIconElement);

    // Get the target element where you want to append the <p> element
    var targetElement = document.getElementById('targetElementId');

    // Append the <p> element to the target element
    
    // Get the target element where you want to append the SVG
    // Append the SVG element to the target element
    

    parentDiv.appendChild(div);
    parentDiv.appendChild(svgElement);
    parentDiv.appendChild(pElement);
  }

function apiExportCall() {
  // Get all the form elements
  var forms = document.getElementsByTagName('form');

  // Initialize an array to store the URL parameters
  var urlParametersArray = [];

  // Iterate over each form
  for (var i = 0; i < forms.length; i++) {
    var form = forms[i];

    // Collect the form data
    var formData = {};
    var inputs = form.getElementsByTagName('input');
    for (var j = 0; j < inputs.length; j++) {
      var input = inputs[j];
      formData[input.name] = input.value;
    }

    // Encode the form data as URL parameters
    var encodedData = Object.keys(formData).map(function(key) {
      return encodeURIComponent(key) + '=' + encodeURIComponent(formData[key]);
    }).join('&');

    // Add the encoded form data to the URL parameters array
    urlParametersArray.push(encodedData);
  }

  // Join the URL parameters with ampersands (&)
  var urlParameters = urlParametersArray.join('&');

  // Create the final URL
  var url = 'http://localhost:8000/channel/excel?' + urlParameters;

  window.location.href = url;
}

function deleteFileObjectById(id) {

  const container = document.getElementById('li ' + id);

  const itemToRemove = document.getElementById(id);

  const newItemElement = document.createElement('box-icon');

  newItemElement.id = id;
  newItemElement.name = 'list-ul';
  newItemElement.color ='#ffffff';

  itemToRemove.remove();

  container.appendChild(newItemElement);
  
  // fetch(`${apiUrl}/${id}`, {
  //   method: 'DELETE',
  //   headers: {
  //     'Content-Type': 'application/json',
  //     // Add any additional headers if required
  //   },
  // })
  //   .then(response => {
  //     if (response.ok) {
  //       console.log('Object deleted successfully.');
  //       // Perform any additional actions upon successful deletion
  //     } else {
  //       console.error('Failed to delete object.');
  //       // Handle the error condition accordingly
  //     }
  //   })
  //   .catch(error => {
  //     console.error('An error occurred while deleting the object:', error);
  //     // Handle any network or other errors
  //   });
}