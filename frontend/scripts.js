COLORS = {
   "NEUTRAL": "#d4ffff",
   "HAPPY": "#feffa8",
   "SAD": "#a8b5ff",
   "ANGRY": "#ff8c8c",
   "SURPRISED": "#fcb1fb",
   "SCARED": "#b69fc7",
   "CURIOUS": "#bbf0d4",
   "BORING": "#d6f0bb",
}

document.getElementById('analyze-btn').addEventListener('click', async function () {
   document.getElementById('result-loading').classList.remove('hidden');
   // Start the fetch request
   let data = await query(`http://localhost:5000/classify/${document.getElementById('youtube-link').value}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
   });

   // Hide the loading spinner
   document.getElementById('result-loading').classList.add('hidden');
   if (data.status === 200) {
      // Success: handle the response data
      // Example: display result
      annouceDisplay("Success", 'green');
   } else if (data.status === 404) {
      // Not found: handle accordingly
      annouceDisplay("404: Not found", 'red');
   } else if (data.status === 400) {
      // Bad request: handle accordingly
      annouceDisplay("400: Bad request", 'red');
   } else if (data.status === 405) {
      // Method not allowed: handle accordingly
      annouceDisplay("405 ???", "red");
   } else if (data.status === 500) {
      // Server error: handle accordingly
      annouceDisplay("500 Server error", "red");
   }
   percentages = calculatePercentage(data.data.llm);
   console.log(percentages);

   targets = ["llm", "lstm", "naive-bayes"]

   // For each target, calculate and display percentages in the corresponding div
   targets.forEach(target => {
      let percentages = calculatePercentage(data.data[target]);
      let container = document.getElementById(`${target}`);
      if (container) {
         container.innerHTML = '';
         for (let label in percentages) {
            if (percentages[label] > 0) {
               container.innerHTML += createSpan(label, percentages[label]);
            }
         }
      }
   });

   // Change the #title to the video title
   if (data.data.title) {
      document.getElementById('title').innerText = data.data.title;
   } else {
      document.getElementById('title').innerText = "No title found";
   }

   // remove the transparent from the #result-container
   document.getElementById('result-container').classList.remove('transparent');

   document.getElementById('inspect').innerHTML = generateInspect(data.data, 10);
   document.getElementById('inspect').classList.remove('transparent');
});


function annouceDisplay(error, color) {
   /*
   Placeholder for displaying error messages.
   This function can be customized to show errors in a specific format or location.
   */
   document.getElementById('error-container').innerHTML = `Announce: ${error}`;
   document.getElementById('error-container').style.color = color;

}

async function query(url, options) {
   /*
   Placeholder for fetching data.
   Returns an object with HTTP status code and response data.
   */
   try {
      const response = await fetch(url, options);
      const data = await response.json();
      return {
         status: response.status,
         data: data
      };
   } catch (error) {
      return {
         status: 500,
         data: { error: error.message }
      };
   }
}

function calculatePercentage(list) {
   /*
   Turn a list of items into a percentage list of those items.
   Each item in the list is divided by the total sum of the list,
   */
   count = {
      "NEUTRAL": 0,
      "HAPPY": 0,
      "SAD": 0,
      "ANGRY": 0,
      "SURPRISED": 0,
      "SCARED": 0,
      "CURIOUS": 0,
      "BORING": 0
   }
   let total = 0;
   for (let item of list) {
      if (item in count) {
         count[item] += 1;
         total += 1;
      }
   }
   let percentages = {};
   ROUNDED = 1
   for (let key in count) {
      if (total > 0) {
         const factor = Math.pow(10, ROUNDED);
         percentages[key] = Math.round((count[key] / total) * 100 * factor) / factor;
      } else {
         percentages[key] = 0;
      }
   }

   // Sort percentages by value in descending order
   percentages = Object.fromEntries(
      Object.entries(percentages).sort(([, a], [, b]) => b - a)
   );
   return percentages;
}

function createSpan(label, percentage) {
   // CSS class for emotion span:
   /*
   .emotion-span {
      background-color: var(--emotion-color, #eee);
      border-radius: 8px;
      padding: 4px 10px;
      margin: 2px;
      display: inline-block;
   }
   */
   return `<span class="emotion-span" style="background-color: ${COLORS[label] || '#eee'};">${label}: ${percentage}%</span>`;
}

function textSpan(text, bgColor, txtColor) {
   return `<span class="emotion-span" style="background-color: ${bgColor}; color: ${txtColor};">${text}</span>`;
}

function generateInspect(data, length) {
   // Randomly get a subset of data for inspection
   // data is a dictionary with keys of raw_comments, lstm, naive-bayes, llm each is a list
   let randomIDs = [];
   while (randomIDs.length < length) {
      let randomID = Math.floor(Math.random() * data.raw_comments.length);
      if (!randomIDs.includes(randomID)) {
         randomIDs.push(randomID);
      }
   }


   let inspectHTML = '';
   randomIDs.forEach(id => {
      inspectHTML += `<div class="inspect-item">
         ${textSpan(data.commentor[id], "#696969", "#fff")}
         <p>${data.raw_comments[id]}</p>
         <div>
         ${textSpan('LSTM: ' + data.lstm[id], COLORS[data.lstm[id]] || '#eee', '#000')}
         ${textSpan('Naive Bayes: ' + data['naive-bayes'][id], COLORS[data['naive-bayes'][id]] || '#eee', '#000')}
         ${textSpan('LLM: ' + data.llm[id], COLORS[data.llm[id]] || '#eee', '#000')}
         </div>
      </div>`;
   });
   return inspectHTML;
}