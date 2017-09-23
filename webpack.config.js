const path = require('path');

module.exports = {
  entry: './kudos/static/js/options.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'kudos/static/dist')
  }
};
