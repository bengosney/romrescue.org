
module.exports = function (grunt) {

  require('load-grunt-tasks')(grunt);
  require('google-closure-compiler').grunt(grunt);

  grunt.initConfig({
    postcss: {
      options: {
        map: false,
        processors: [
          require('postcss-import')(),
          require('pixrem')(),
          require('autoprefixer')({browsers: 'last 3 versions'}),
          require('postcss-flexibility')(),
          require('css-mqpacker')({sort: true}),
          require('cssnano')({zindex: false})
        ]
      },
      dist: {
        src: 'pages/static/pages/css/*.css'
      }
    },
    compass: {
      dist: {
        options: {
          sassDir: 'scss',
          cssDir: 'pages/static/pages/css',
          environment: 'production'
        }
      },
      dev: {
        options: {
          sassDir: 'scss',
          cssDir: 'pages/static/pages/css'
        }
      }
    },
    sass_globbing: {
      sass: {
        files: {
          'scss/_imports.scss': 'scss/partials/**/*.scss'
        },
        options: {
          useSingleQuotes: false,
          signature: '// 00Dog'
        }
      },
    },
    webfont:{
      icons: {
	src: 'icons/build/**/*.svg',
	dest: 'pages/static/pages/fonts',
	options: {
          template: 'icons/template.css',
          stylesheet: 'scss',
          htmlDemo: false,
          relativeFontPath: '/static/pages/fonts/',
          destCss: 'scss/partials/',
          customOutputs: [{
	    template: 'icons/json.template',
	    dest: 'icons/icons.json'
	  },
          {
	    template: 'icons/python.template',
	    dest: 'icons/icons.py'
	  }]
	}
      }
    },
    babel: {
      options: {
        plugins: ['transform-react-jsx'], // npm install babel-plugin-transform-react-jsx
        presets: ['es2015', 'react'] // npm install babel-preset-es2015 babel-preset-react
      },
      jsx: {
        files: [{
          expand: true,
          cwd: 'js/jsx',
          src: ['*.jsx'],
          dest: 'js/compiled',
          ext: '.js'
        }]
      }
    },
    jshint: {
      all: ['js/build/**/*.js']
    },
    concat: {
      options: {
        separator: "\n;"
      },
      js: {
        src: ['js/external/**/*.js', 'js/polyfill/**/*.js', 'js/build/**/*.js', 'js/compiled/**/*.js'],
        dest: 'pages/static/pages/js/script.js'
      }
    },
    flake8: {
      options: {
        errorsOnly: true
      },
      src: [
        '**/*.py',
        '!**/migrations/*.py',
        '!node_modules/**/*.py',
        '!icons/**/*.py'
      ],
    },
    'closure-compiler': {
      jscompile: {
        files: {
          'media/map.min.js': ['js/build/**/*.js']
        },
        options: {
          compilation_level: 'SIMPLE',
          create_source_map: 'media/map.min.js.map'
        }
      }
    },
    watch: {
      scss_compile: {
        files: ['scss/**/*.*'],
        tasks: ['scss'],
        options: {
          spawn: false
        }
      },
      flake: {
        files: ['**/*.py'],
        tasks: ['flake8'],
      },
      js: {
        files: ['js/build/**/*', 'js/external/**/*', 'js/polyfils/**/*', 'js/compiled/**/*'],
        tasks: ['js']
      },
      jsx:{
        files: ['js/jsx/**/*'],
        tasks: ['babel']
      },
      icons: {
        files: ['icons/build/**/*'],
        tasks: ['webfont']
      }
    },
  });

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('icons', ['webfont']);
  grunt.registerTask('scss', ['sass_globbing', 'compass:dist', 'postcss:dist']);
  grunt.registerTask('js', ['jshint', /*'closure-compiler',*/ 'concat']);
  grunt.registerTask('css', ['scss']);
  grunt.registerTask('compile', ['icons', 'scss', 'js']);
};
