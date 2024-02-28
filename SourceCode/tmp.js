//dummy, full js code is inside scraper functions.py, this was used as a basic reference  for myself when coding
const axios = require('axios');
const cheerio = require('cheerio');

const url = 'https://example.com'; // Replace with the URL you want to scrape

axios.get(url)
  .then(response => {
    const html = response.data;
    const $ = cheerio.load(html);
    const articles = [];

    // Example: Extract 'article' elements or any relevant tag or class
    $('article').each(function() {
      const title = $(this).find('h2').text(); // Assuming titles are in <h2>
      const link = $(this).find('a').attr('href'); // Assuming a direct link is available

      articles.push({
        title,
        link
      });
    });

    console.log(articles);
  })
  .catch(error => {
    console.error('Error fetching the page:', error);
  });

