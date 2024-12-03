describe('load_cities', function() {
  let pathFinder;

  // Mock fetch function before each test
  beforeEach(function() {
    // Reset the pathFinder instance before each test
    pathFinder = new PathFinder();

    // Mock the fetch function to simulate API response
    global.fetch = function(url) {
      return new Promise((resolve, reject) => {
        // Check URL to mock specific API call
        if (url === 'https://api.group2.proxy.devops-pse.users.h-da.cloud/cities') {
          resolve({
            ok: true,
            json: () => {
              return Promise.resolve({
                cities: [
                  { name: 'Markarth', position_x: 1, position_y: 2 },
                  { name: 'Karthwasten', position_x: 3, position_y: 4 }
                ]
              });
            }
          });
        } else {
          reject(new Error('Unknown API endpoint'));
        }
      });
    };
  });

  it('should load cities and populate select options', function(done) {
    // Mocking DOM elements
    document.body.innerHTML = `
      <ul id="endpoint_list"></ul>
      <select id="startpoint"></select>
      <select id="endpoint"></select>
    `;

    // Call the method that triggers the fetch
    pathFinder.load_cities();

    // Wait for the asynchronous fetch call to complete
    setTimeout(() => {
      // Check that the cities are loaded correctly into the select options
      const startpointOptions = document.getElementById('startpoint').children;
      const endpointOptions = document.getElementById('endpoint').children;

      expect(startpointOptions.length).to.equal(3); // 2 cities + 1 default option
      expect(endpointOptions.length).to.equal(3); // 2 cities + 1 default option

      expect(startpointOptions[1].textContent).to.equal('Markarth');
      expect(endpointOptions[2].textContent).to.equal('Karthwasten');

      done();
    }, 100); // Timeout for async operation
  });
});
