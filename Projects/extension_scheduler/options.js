// options.js

let previousOptions = {};

// Function to get the service worker registration asynchronously
async function getServiceWorkerRegistration() {
  const registration = await navigator.serviceWorker.getRegistration();
  return registration ? registration.active : null;
}

function getTotalMinutesSinceMidnight(timeString) {
  const [time, amPm] = timeString.split(' ');
  const [hours, minutes] = time.split(':').map(Number);

  // Adjust the hours to 24-hour format based on AM/PM
  let adjustedHours = hours;
  if (amPm === 'PM' && hours !== 12) {
    adjustedHours += 12;
  } else if (amPm === 'AM' && hours === 12) {
    adjustedHours = 0;
  }

  const totalMinutes = adjustedHours * 60 + minutes;
  return totalMinutes;
}

// Function to convert time to 24-hour format
function convertTo24HourFormat(hour, amPm) {
  if (amPm === 'PM' && hour !== 12) {
    hour += 12;
  } else if (amPm === 'AM') {
    if (hour === 12) {
      hour = 0; // Special case for 12:00 AM
    }
  }
  return hour;
}

function padWithLeadingZero(number) {
  return number.toString().padStart(2, '0');
}

// Event listeners to handle custom arrow buttons for number inputs
function addArrowButtonListeners() {
  const arrowButtons = document.querySelectorAll('.arrow-button');
  arrowButtons.forEach((button) => {
    button.addEventListener('click', handleArrowButtonClick);
  });
}

function handleArrowButtonClick(event) {
  const button = event.target;
  const timeContainer = button.closest('.time-input');
  const inputField = timeContainer.querySelector('input[type="number"]');
  const step = parseInt(inputField.step) || 1;
  const maxHour = 12;
  const maxMinute = 59;

  if (button.id.endsWith('Increment')) {
    if (inputField.classList.contains('hour-input')) {
      if (parseInt(inputField.value) === maxHour) {
        // If the current value is the maxHour, set it back to 1
        inputField.value = 1;
      } else {
        inputField.stepUp(step);
      }
    } else if (inputField.classList.contains('minute-input')) {
      if (parseInt(inputField.value) === maxMinute) {
        // If the current value is the maxMinute, set it back to 0
        inputField.value = 0;
      } else {
        inputField.stepUp(step);
      }
    } else {
      inputField.stepUp(step);
    }
  } else if (button.id.endsWith('Decrement')) {
    if (inputField.classList.contains('hour-input')) {
      if (parseInt(inputField.value) === 1) {
        // If the current value is 1, set it to maxHour
        inputField.value = maxHour;
      } else {
        inputField.stepDown(step);
      }
    } else if (inputField.classList.contains('minute-input')) {
      if (parseInt(inputField.value) === 0) {
        // If the current value is 0, set it to maxMinute
        inputField.value = maxMinute;
      } else {
        inputField.stepDown(step);
      }
    } else {
      inputField.stepDown(step);
    }
  }

  // Add leading zero if the value is a single digit
  inputField.value = padWithLeadingZero(inputField.value);
}

// Function to update the active days checkboxes in the options UI
function updateActiveDaysCheckboxes(activeDays) {
  const activeDaysCheckboxes = document.querySelectorAll('.active-days-container input[type="checkbox"]');
  activeDaysCheckboxes.forEach(function (checkbox) {
    const day = checkbox.getAttribute('value');
    checkbox.checked = activeDays.includes(day);
  });
}

// Function to populate dropdown select element with options
function populateDropdown(selectId, start, end, defaultValue) {
  const select = document.getElementById(selectId);
  select.innerHTML = '';
  for (let i = start; i <= end; i++) {
    const option = document.createElement('option');
    const value = String(i).padStart(2, '0');
    option.value = value;
    option.textContent = value;
    select.appendChild(option);
  }

  // Handle special case for '12 PM'
  if (defaultValue === 12) {
    select.value = '12';
  } else {
    select.value = String(defaultValue).padStart(2, '0');;
  }
}

// Function to update the options on the HTML document
function updateDocumentOptions(options) {
  const checkedExtensions = options.checkedExtensions || [];
  const startHour = options.startHour || '08';
  const startMinute = options.startMinute || '00';
  const startAmPm = options.startAmPm || 'AM';
  const endHour = options.endHour || '04';
  const endMinute = options.endMinute || '00';
  const endAmPm = options.endAmPm || 'PM';

  // Update the extension checkboxes
  const extensionCheckboxes = document.querySelectorAll('#extensionList input[type="checkbox"]');
  extensionCheckboxes.forEach(function (checkbox) {
    const extensionId = checkbox.getAttribute('data-extension-id');
    checkbox.checked = checkedExtensions.includes(extensionId);
  });

  // Update the start time fields
  document.getElementById('startHour').value = startHour;
  document.getElementById('startMinute').value = startMinute;
  document.getElementById('startAmPm').value = startAmPm;

  // Update the end time fields with the correct AM/PM value
  document.getElementById('endHour').value = endHour;
  document.getElementById('endMinute').value = endMinute;
  document.getElementById('endAmPm').value = endAmPm;

  // Update the active days checkboxes with default values if options.activeDays is not defined or not an array
  const activeDays = options.activeDays || ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  const activeDaysCheckboxes = document.querySelectorAll('.active-days-container input[type="checkbox"]');
  activeDaysCheckboxes.forEach(function (checkbox) {
    const day = checkbox.getAttribute('value');
    checkbox.checked = activeDays.includes(day);
  });

  // Additional code to set Monday to Friday checkboxes to checked by default
  const defaultActiveDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  defaultActiveDays.forEach(function (day) {
    const checkbox = document.querySelector(`#activeDaysList input[value="${day}"]`);
    if (checkbox && !activeDays.includes(day)) {
      checkbox.checked = true;
    }
  });
}

// Log a message to the background script
function logToBackgroundConsole(message, data) {
  const logMessage = {
    message: message,
    data: data
  };
  chrome.runtime.sendMessage({ logMessage: JSON.stringify(logMessage) });
}

// Event listener when the DOM content is loaded
document.addEventListener('DOMContentLoaded', async function () {
  const extensionList = document.getElementById('extensionList');
  const selectAllCheckbox = document.getElementById('selectAll');
  const messageContainer = document.getElementById('messageContainer');
  const messageText = document.getElementById('messageText');

  if (extensionList && selectAllCheckbox && messageContainer && messageText) {
    // Get the options from Chrome storage
    chrome.storage.local.get(
      [
        'checkedExtensions',
        'startHour',
        'startMinute',
        'startAmPm',
        'endHour',
        'endMinute',
        'endAmPm',
        'activeDays',
        'extensionsEnabled'
      ],
      function (data) {
        // Get the list of checked extensions from Chrome storage
        const checkedExtensions = data.checkedExtensions || [];

        // Populate dropdown select elements for time selection
        populateDropdown('startHour', '01', '12', data.startHour || '08');
        populateDropdown('startMinute', '00', '59', data.startMinute || '00');
        populateDropdown('endHour', '01', '12', data.endHour || '04');
        populateDropdown('endMinute', '00', '59', data.endMinute || '00');

        // Update the values in the current HTML document
        updateDocumentOptions(data);

        addArrowButtonListeners();

        // Create a Promise to fetch the extensions using chrome.management.getAll
        const extensionsPromise = new Promise((resolve) => {
          chrome.management.getAll(resolve);
        });

        // Wait for the extensionsPromise to resolve with the extensions
        extensionsPromise.then(function (extensions) {

          // Filter and sort the extensions
          const validExtensions = extensions.filter(function (extension) {
            // Filter out extensions installed by Company Policy
            return extension.type === 'extension' && extension.id !== chrome.runtime.id && !extension.installType.includes('admin');
          });

          validExtensions.sort(function (a, b) {
            return a.name.localeCompare(b.name);
          });

          if (validExtensions.length === 0) {
            // If no valid extensions are installed, display the message and hide the extensionList and selectAllCheckbox
            messageText.textContent = 'No valid extensions installed on this browser.';
            messageContainer.style.display = 'block';
            extensionList.style.display = 'none';
            selectAllCheckbox.style.display = 'none';
          } else {
            validExtensions.forEach(function (extension) {
              const listItem = document.createElement('li');
              const checkbox = document.createElement('input');
              checkbox.type = 'checkbox';
              checkbox.checked = checkedExtensions.includes(extension.id);
              checkbox.setAttribute('data-extension-id', extension.id);
              listItem.appendChild(checkbox);

              const icon = document.createElement('img');
              icon.src = extension.icons ? extension.icons[0].url : 'icon-default.png';
              icon.classList.add('extension-icon');
              listItem.appendChild(icon);

              const name = document.createElement('span');
              name.textContent = extension.name;
              listItem.appendChild(name);

              extensionList.appendChild(listItem);
            });

            // Event listener for "Select All" checkbox
            selectAllCheckbox.addEventListener('change', function (event) {
              const isChecked = event.target.checked;
              const extensionCheckboxes = document.querySelectorAll('#extensionList input[type="checkbox"]');
              extensionCheckboxes.forEach(function (checkbox) {
                checkbox.checked = isChecked;
              });
            });
          }
        });
        previousOptions = { ...data };
      }
    );
  }

  // Save options when the Save button is clicked
  document.getElementById('saveButton').addEventListener('click', function () {
    saveOptions();
   });
});

// Function to check if any changes have been made to the options
function areChangesMade() {
  const startHour = document.getElementById('startHour').value;
  const startMinute = document.getElementById('startMinute').value;
  const startAmPm = document.getElementById('startAmPm').value;

  const endHour = document.getElementById('endHour').value;
  const endMinute = document.getElementById('endMinute').value;
  const endAmPm = document.getElementById('endAmPm').value;

  const checkedExtensionsCheckboxes = document.querySelectorAll('#extensionList input[type="checkbox"]:checked');
  const checkedExtensions = Array.from(checkedExtensionsCheckboxes).map((checkbox) => checkbox.getAttribute('data-extension-id'));

  const activeDayCheckboxes = document.querySelectorAll('input[name="activeDays"]:checked');
  const activeDays = Array.from(activeDayCheckboxes).map((checkbox) => checkbox.value);

  // Check if any of the options have changed
  return (
    startHour !== previousOptions.startHour ||
    startMinute !== previousOptions.startMinute ||
    startAmPm !== previousOptions.startAmPm ||
    endHour !== previousOptions.endHour ||
    endMinute !== previousOptions.endMinute ||
    endAmPm !== previousOptions.endAmPm ||
    !arraysEqual(checkedExtensions, previousOptions.checkedExtensions) ||
    !arraysEqual(activeDays, previousOptions.activeDays)
    // Add more checks if you have other options that can be changed
  );
}

// Function to compare two arrays for equality
function arraysEqual(arr1, arr2) {
  if (arr1.length !== arr2.length) {
    return false;
  }
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) {
      return false;
    }
  }
  return true;
}

// Event listener for the beforeunload event (Check if there are unsaved changes when closing page)
window.addEventListener('beforeunload', function (event) {
  // Check if changes have been made
  if (areChangesMade()) {
    // Display a confirmation message to the user
    const confirmationMessage = 'You have unsaved changes. Are you sure you want to leave the page?';
    event.returnValue = confirmationMessage; // This will display a browser-specific confirmation dialog
    return confirmationMessage; // For some older browsers
  }
});

// Function to save options to Chrome storage
function saveOptions() {
  // Get the checked extensions from the checkboxes
  const extensionCheckboxes = document.querySelectorAll('#extensionList input[type="checkbox"]:checked');
  const checkedExtensions = Array.from(extensionCheckboxes).map(function (checkbox) {
    return checkbox.getAttribute('data-extension-id');
  });

  // Get the active days from the checkboxes
  const activeDayCheckboxes = document.querySelectorAll('input[name="activeDays"]:checked');
  const activeDays = Array.from(activeDayCheckboxes).map(function (checkbox) {
    return checkbox.value;
  });

  // If no active days are checked, use the default active days (M-F)
  if (activeDays.length === 0) {
    activeDays.push(...['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']);
  }


  const startHour = document.getElementById('startHour').value;
  const startMinute = document.getElementById('startMinute').value;
  const startAmPm = document.getElementById('startAmPm').value;

  let endHour = document.getElementById('endHour').value;
  let endMinute = document.getElementById('endMinute').value;
  let endAmPm = document.getElementById('endAmPm').value;

  // Store the current values as previously saved values
  const previousStartHour = startHour;
  const previousStartMinute = startMinute;
  const previousStartAmPm = startAmPm;

  const previousEndHour = endHour;
  const previousEndMinute = endMinute;
  const previousEndAmPm = endAmPm;

  // Calculate isWithinActiveTimeRange based on the current time and options
  const currentDay = new Date().toLocaleDateString('en-US', { weekday: 'long' });
  const currentHour = new Date().getHours();
  const currentMinute = new Date().getMinutes();
  const currentMinutes = currentHour * 60 + currentMinute;
  const adjustedStartMinutes = getTotalMinutesSinceMidnight(`${startHour}:${startMinute} ${startAmPm}`);
  let adjustedEndMinutes = getTotalMinutesSinceMidnight(`${endHour}:${endMinute} ${endAmPm}`);

  let isWithinActiveTimeRange = false;

  if (adjustedEndMinutes < adjustedStartMinutes) {
    // Two time ranges: from start time to midnight and from midnight to end time
    isWithinActiveTimeRange =
      (currentMinutes >= adjustedStartMinutes && currentMinutes <= 24 * 60) || // From start time to midnight
      (currentMinutes >= 0 && currentMinutes < adjustedEndMinutes); // From midnight to end time
  } else {
    // Normal time range
    isWithinActiveTimeRange = currentMinutes >= adjustedStartMinutes && currentMinutes < adjustedEndMinutes;
  }

  // Calculate extensionsEnabled based on isWithinActiveTimeRange and other conditions
  const extensionsEnabled = isWithinActiveTimeRange && activeDays.includes(currentDay);

  const options = {
    checkedExtensions: checkedExtensions,
    startHour: startHour,
    startMinute: startMinute,
    startAmPm: startAmPm,
    endHour: endHour,
    endMinute: endMinute,
    endAmPm: endAmPm,
    activeDays: activeDays,
    extensionsEnabled: extensionsEnabled
  };

  // Validate the End Time against the Start Time
  if (
    ((startHour === endHour) && (startMinute === endMinute) && (startAmPm === endAmPm)) // If Start Time is same as End Time
  ) {
    const statusText = document.getElementById('statusText');
    statusText.textContent = 'Error: End Time cannot be the same as Start Time.';
    statusText.style.display = 'block';
    // Clear the prompt after 5 seconds
    setTimeout(() => {statusText.style.display = 'none';}, 5000);
    return; // Abort saving options if the validation fails
  } else if (
    // If Start Time is PM and End Time is AM
    ((startAmPm === 'PM' && endAmPm === 'AM') ||
    // If both Start Time and End Time are PM, and End Hour is less than Start Hour (except when Start Hour is 12)
    ((endAmPm === 'PM' && startAmPm === 'PM') && (endHour < startHour) && (startHour != 12)) ||
    // If both Start Time and End Time are AM, and End Hour is less than Start Hour (except when Start Hour is 12)
    ((endAmPm === 'AM' && startAmPm === 'AM') && (endHour < startHour) && (startHour != 12)) ||
    // If both Start Time and End Time are PM, and End Hour is equal to Start Hour, and End Minute is less than or equal to Start Minute
    ((endAmPm === 'PM' && startAmPm === 'PM') && (endHour === startHour) && (endMinute <= startMinute)) ||
    // If both Start Time and End Time are AM, and End Hour is equal to Start Hour, and End Minute is less than or equal to Start Minute
    ((endAmPm === 'AM' && startAmPm === 'AM') && (endHour === startHour) && (endMinute <= startMinute)) ||
    // If Start Time is PM and End Time is AM, and End Hour is 12, and either (Start Hour is 12 and End Minute is less than Start Minute) or Start Hour is not 12
    ((endAmPm === 'AM' && startAmPm === 'PM') && (endHour === 12) && (((startHour === 12) && (endMinute < startMinute)) || (startHour != 12))))
  ) {

    if (window.confirm(
    `Scheduler will be active between ${startHour}:${startMinute} ${startAmPm} and midnight, and then between midnight and ${endHour}:${endMinute} ${endAmPm}.
    \n Are you sure that's what you meant to do?`) === false) {
      // If the user clicks "Cancel" in the confirmation dialog, cancel Save
      const statusText = document.getElementById('statusText');
      statusText.textContent = 'Save Canceled.';
      statusText.style.display = 'block';
      // Clear the prompt after 5 seconds
      setTimeout(() => {statusText.style.display = 'none';}, 5000);
      return;
    }
  }

  chrome.storage.local.set(options, function () {

    // Log the values in Chrome storage after save
    chrome.storage.local.get(null, function (data) {
      logToBackgroundConsole('Values in Chrome storage after save:', data);
      // Update the values in the current HTML document
      updateDocumentOptions(data);

      // Update the active days checkboxes after saving options
      updateActiveDaysCheckboxes(activeDays);

      // Notify the background script about the options change
      chrome.runtime.sendMessage({ optionsUpdated: true });
    });

    const statusText = document.getElementById('statusText');
    statusText.textContent = 'Options saved successfully.';
    statusText.style.display = 'block';

    // Notify the service worker about the options change
    getServiceWorkerRegistration().then((worker) => {
      if (worker) {
        worker.postMessage({ optionsUpdated: true });
      }
    });
  });

  previousOptions = { ...options };

  // Clear the prompt after 5 seconds
  setTimeout(() => {
    statusText.style.display = 'none';
  }, 5000);
}


// Add an event listener to receive messages from the background script
chrome.runtime.onMessage.addListener(function (message) {
  if (message.extensionsToggled) {
    // The background script notified about the extension state change
    // Let's update the options page to reflect the changes
    chrome.storage.local.get(null, function (data) {
      updateDocumentOptions(data);
    });
  }
});

