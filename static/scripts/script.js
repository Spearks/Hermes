function addExportToChannel() {
  // delete the buttons
  const buttonAdd = document.getElementById("button-add").cloneNode(true);
  const buttonDown = document.getElementById("button-export").cloneNode(true);

  document.getElementById("button-add").remove();
  document.getElementById("button-export").remove();

  const originalDiv = document.getElementById("form-export");
  const copiedDiv = originalDiv.cloneNode(true);

  // get the parent element of form-export
  const parentElement = document.getElementById("form");

  // add a margin top of 5 rem
  copiedDiv.classList.add("mt-5");
  copiedDiv.appendChild(buttonAdd);
  copiedDiv.appendChild(buttonDown);

  parentElement.appendChild(copiedDiv);
}

function apiExportCall() {
  // Get all the forms elements
  var forms = document.getElementsByTagName("form");

  // Get the current channel of the export
  const channel = window.location.pathname.split("/").pop();

  // Initialize an array to store the URL parameters
  var urlParametersArray = [];

  // Iterate over each form
  for (var i = 0; i < forms.length; i++) {
    var form = forms[i];

    // Collect the form data
    var formData = {};
    var inputs = form.getElementsByTagName("input");
    for (var j = 0; j < inputs.length; j++) {
      var input = inputs[j];
      formData[input.name] = input.value;
    }

    // Encode the form data as URL parameters
    var encodedData = Object.keys(formData)
      .map(function (key) {
        return (
          encodeURIComponent(key) + "=" + encodeURIComponent(formData[key])
        );
      })
      .join("&");

    // Add the encoded form data to the URL parameters array
    urlParametersArray.push(encodedData);
  }

  urlParametersArray.push("channel=" + channel);

  // Join the URL parameters with ampersands (&)
  var urlParameters = urlParametersArray.join("&");

  // Create the final URL
  var url = h_url + "/channel/export/file/xlsx?" + urlParameters;

  window.location.href = url;
}

function showGrafanaIframe(iframeSrc, id, size, divToRemove) {
  // Get the div to append the iframe
  const divToAppend = document.getElementById(id);

  // Remove the div specified in divToRemove
  const divToRemoveElement = document.getElementById(divToRemove);
  if (divToRemoveElement) {
    divToRemoveElement.remove();
  } else {
    console.error(`Element with ID '${divToRemove}' not found.`);
  }

  // Create the iframe element
  const iframe = document.createElement("iframe");
  iframe.classList.add("w-full", size);
  iframe.id = "ifrm";
  iframe.src = iframeSrc;

  // Append the iframe to the divToAppend
  divToAppend.appendChild(iframe);
}

function deleteFileObjectById(id) {
  const container = document.getElementById("li " + id);

  const itemToRemove = document.getElementById(id);

  const newItemElement = document.createElement("box-icon");

  newItemElement.id = id;
  newItemElement.name = "list-ul";
  newItemElement.color = "#ffffff";

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

// Get the select element by its ID
const selectElement = document.getElementById("times");

// Function to handle the change event
function handleSelectChange() {
  // Get the selected value
  const selectedValue = selectElement.value;

  // Perform some action based on the selected value
  switch (selectedValue) {
    case "5m":
      console.log("You selected 5 minutes.");
      break;
    case "10m":
      console.log("You selected 10 minutes.");
      break;
    case "1d":
      console.log("You selected 1 day.");
      break;
    case "3d":
      console.log("You selected 3 days.");
      break;
    default:
      console.log("You selected 120 seconds.");
      break;
  }
}

// Add event listener to the select element
selectElement.addEventListener("change", handleSelectChange);

function activateSelectListOnChannels() {
  var channelInputs = document.querySelectorAll("input.channel");

  channelInputs.forEach(function (input) {
    input.style.display = "inline-block";
  });
}

// TODO: fix it
function exportChannelsOnMultipleView() {
  // Get all the form elements
  var forms = document.getElementsByTagName("form");

  // Initialize an array to store the URL parameters
  var urlParametersArray = [];

  // Iterate over each form
  for (var i = 0; i < forms.length; i++) {
    var form = forms[i];
    var formDataTeste = new FormData(form);
    console.log(formDataTeste);

    // Collect the form data
    var formData = {};

    // Collect input values
    var inputs = form.getElementsByTagName("input");
    for (var j = 0; j < inputs.length; j++) {
      var input = inputs[j];
      formData[input.name] = input.value;
    }

    // Collect select values
    var selects = form.getElementsByTagName("select");
    for (var k = 0; k < selects.length; k++) {
      var select = selects[k];
      formData[select.name] = select.value;
    }

    // Store formData in the urlParametersArray
    urlParametersArray.push(formData);
  }

  // const combinedParams = urlParametersArray
  //   .map(data => Object.keys(data)
  //     .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(data[key])}`)
  //     .join('&')
  //   )
  //   .join('&'); // Join individual parameter strings

  const combinedParams = urlParametersArray.reduce((result, data) => {
    Object.keys(data).forEach((key) => {
      result[key] = data[key];
    });
    return result;
  }, {});

  console.log(combinedParams);
  console.log(urlParametersArray);
}

function getAllInputChannels() {
  var channelInputs = document.querySelectorAll("input.channel");

  var channels = [];

  // Get channels and insert into to "channels"
  channelInputs.forEach(function (input) {
    var id = input.id;
    if (input.checked) {
      channels.push(id);
    }
  });

  // Encode the url
  var encodedChannels = channels
    .map(function (id) {
      return "channel=" + encodeURIComponent(id);
    })
    .join("&");

  var url = h_url + "/channel/export/view/multiple?" + encodedChannels;

  window.location.href = url;
}
