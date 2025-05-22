document.getElementById('analyze-btn').addEventListener('click', async function() {
   document.getElementById('result-loading').classList.remove('hidden');
   // Start the fetch request
   let data = await query('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
         comment: document.getElementById('youtube-link').value
      })
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
   console.log(data);
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


