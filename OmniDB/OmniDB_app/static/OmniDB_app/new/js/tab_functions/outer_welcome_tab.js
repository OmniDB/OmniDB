var v_createWelcomeTabFunction = function(p_index,p_create_query_tab = true, p_name = false, p_tooltip_name = false) {
  // Removing the last `add` tab
  v_connTabControl.removeLastTab();

  var v_tab = v_connTabControl.createTab({
    p_icon: '<i class="fas fa-hand-spock"></i>',
    p_name: 'Welcome',
    p_selectFunction: function() {
      document.title = 'Welcome toOmniDB'
      $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips
    },
    p_close: false,// Replacing default close icon with contextMenu.
    p_closeFunction: function(e,p_tab) {
      var v_this_tab = p_tab;
      beforeCloseTab(e,
        function() {
          v_this_tab.removeTab();
        });
    },
    p_rightClickFunction: function(e) {
      var v_option_list = [
        {
          text: '<p class=\"mb-0 text-danger\">Close Welcome Tab</p>',
          action: function() {
            if (v_tab.closeFunction!=null) {
              v_tab.closeFunction(e,v_tab);
            }
          }
        }
      ];
      customMenu(
        {
          x:e.clientX+5,
          y:e.clientY+5
        },
        v_option_list,
        null);
    },
    p_tooltip_name: '<h5 class="my-1">Welcome to OmniDB</h5>'
  });

  v_connTabControl.selectTab(v_tab);

  var v_width = Math.ceil((300/window.innerWidth)*100);
  var v_complement_width = 100 - v_width;

  var v_animated_omnis =
  `<svg
      class="animated-omnis"

      version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
      x="0px" y="0px"
      width="82.333px" height="82.333px"
      viewBox="0 0 82.333 82.333" enable-background="new 0 0 82.333 82.333"
      xml:space="preserve"
  >
      <g class="animated-omnis__icon-grid animated-omnis__group--to-blue">
          <path fill="#878FC6" d="M57.694,31.129c-1.484-2.352-3.474-4.342-5.825-5.823c0.646,1.263,1.214,2.643,1.691,4.129
              C55.049,29.915,56.43,30.486,57.694,31.129z"/>
          <path fill="#878FC6" d="M43.292,22.507v5.234c2.323,0.072,4.553,0.333,6.649,0.762c-0.969-2.344-2.205-4.237-3.614-5.531
              C45.343,22.736,44.331,22.58,43.292,22.507z"/>
          <path fill="#878FC6" d="M57.692,50.87c-1.265,0.644-2.643,1.215-4.132,1.691c-0.477,1.489-1.046,2.867-1.691,4.132
              C54.221,55.211,56.21,53.221,57.692,50.87z"/>
          <path fill="#878FC6" d="M60.188,44.681c-0.359-0.742-0.612-1.537-0.744-2.381h-4.192c-0.072,2.322-0.332,4.551-0.756,6.645
              c2.344-0.969,4.238-2.207,5.532-3.618C60.08,45.11,60.145,44.9,60.188,44.681z"/>
          <path fill="#878FC6" d="M60.029,36.675c-1.293-1.414-3.187-2.652-5.534-3.624c0.424,2.097,0.684,4.325,0.756,6.647h4.192
              c0.132-0.844,0.385-1.639,0.747-2.378C60.145,37.101,60.08,36.889,60.029,36.675z"/>
          <path fill="#878FC6" d="M52.168,42.3h-8.875v8.873c2.79-0.092,5.421-0.475,7.782-1.094C51.693,47.718,52.076,45.09,52.168,42.3z"/>
          <path fill="#878FC6" d="M43.292,39.699h8.875c-0.092-2.79-0.475-5.421-1.094-7.782c-2.361-0.619-4.992-1.002-7.782-1.094V39.699z"
              />
          <path fill="#878FC6" d="M43.292,59.493c1.039-0.072,2.05-0.229,3.036-0.466c1.409-1.296,2.645-3.187,3.614-5.531
              c-2.096,0.427-4.327,0.687-6.649,0.759V59.493z"/>
          <path fill="#878FC6" d="M29.499,48.945c-0.427-2.094-0.687-4.322-0.759-6.645H23.5c0.071,1.036,0.228,2.046,0.462,3.026
              C25.257,46.741,27.152,47.976,29.499,48.945z"/>
          <path fill="#878FC6" d="M40.695,22.507c-1.038,0.072-2.05,0.229-3.034,0.465c-1.409,1.294-2.645,3.188-3.612,5.528
              c2.096-0.426,4.324-0.687,6.646-0.759V22.507z"/>
          <path fill="#878FC6" d="M40.695,30.823c-2.789,0.092-5.419,0.475-7.779,1.094c-0.621,2.361-1.002,4.992-1.094,7.782h8.873V30.823z"
              />
          <path fill="#878FC6" d="M32.123,25.304c-2.353,1.481-4.344,3.472-5.827,5.822c1.265-0.643,2.645-1.214,4.135-1.691
              C30.91,27.947,31.479,26.566,32.123,25.304z"/>
          <path fill="#878FC6" d="M40.695,59.493v-5.238c-2.322-0.072-4.552-0.332-6.646-0.759c0.967,2.345,2.202,4.238,3.612,5.531
              C38.646,59.263,39.657,59.42,40.695,59.493z"/>
          <path fill="#878FC6" d="M23.499,39.699h5.241c0.071-2.322,0.332-4.551,0.759-6.647c-2.348,0.969-4.243,2.21-5.538,3.624
              C23.727,37.656,23.571,38.665,23.499,39.699z"/>
          <path fill="#878FC6" d="M32.123,56.695c-0.644-1.265-1.213-2.643-1.691-4.131c-1.489-0.478-2.868-1.049-4.133-1.691
              C27.781,53.223,29.771,55.213,32.123,56.695z"/>
          <path fill="#878FC6" d="M40.695,42.3h-8.873c0.092,2.79,0.475,5.418,1.094,7.779c2.359,0.619,4.99,1.002,7.779,1.094V42.3z"/>
      </g>
      <g class="animated-omnis__icon-external animated-omnis__group--to-blue">
          <g class="animated-omnis__icon-external__rings">
              <path fill="#878FC6" d="M36.436,14.434c0.642,1.11,0.979,2.306,1.082,3.505c1.451-0.281,2.944-0.438,4.477-0.438
                  c10.299,0,19.03,6.635,22.203,15.854c1.094-0.513,2.301-0.823,3.59-0.823c0.431,0,0.846,0.064,1.26,0.127
                  c-3.561-11.562-14.325-19.967-27.052-19.967c-2.165,0-4.264,0.266-6.291,0.726C35.961,13.743,36.223,14.065,36.436,14.434z"/>
              <path fill="#878FC6" d="M21.771,59.104c0.646-1.115,1.519-2.007,2.513-2.695c-3.58-4.107-5.765-9.463-5.783-15.339
                  c0-0.022-0.006-0.044-0.006-0.068c0-0.019,0.005-0.036,0.005-0.055c0.013-5.874,2.193-11.227,5.766-15.339
                  c-0.99-0.689-1.854-1.593-2.497-2.706c-0.211-0.366-0.356-0.747-0.508-1.127c-4.685,5.052-7.572,11.795-7.572,19.227
                  c0,7.436,2.889,14.179,7.576,19.228C21.415,59.851,21.561,59.468,21.771,59.104z"/>
              <path fill="#878FC6" d="M67.787,49.47c-1.289,0-2.499-0.311-3.592-0.826c-3.175,9.222-11.901,15.853-22.2,15.853
                  c-1.535,0-3.031-0.159-4.483-0.438c-0.103,1.202-0.432,2.401-1.072,3.515c-0.212,0.368-0.472,0.687-0.728,1.01
                  c2.023,0.46,4.121,0.725,6.283,0.725c12.728,0,23.492-8.403,27.055-19.965C68.632,49.405,68.218,49.47,67.787,49.47z"/>
          </g>
          <g class="animated-omnis__icon-external__spheres animated-omnis__group--to-darkblue">
              <path fill="#525678" d="M73.462,41.001c0-3.137-2.539-5.678-5.676-5.678s-5.683,2.541-5.683,5.678s2.546,5.674,5.683,5.674
                  S73.462,44.138,73.462,41.001z"/>
              <path fill="#525678" d="M26.262,13.754c-2.718,1.566-3.647,5.033-2.079,7.753c1.566,2.715,5.042,3.645,7.757,2.079
                  c2.718-1.568,3.645-5.045,2.079-7.755C32.446,13.116,28.979,12.181,26.262,13.754z"/>
              <path fill="#525678" d="M26.267,68.256c2.72,1.568,6.187,0.639,7.755-2.076c1.566-2.715,0.636-6.189-2.077-7.755
                  c-2.72-1.571-6.191-0.639-7.752,2.074C22.622,63.219,23.549,66.691,26.267,68.256z"/>
          </g>
      </g>
  </svg>`;

  // Intro html string
  let v_html_intro =
  '<h1 class="mb-4" style="padding-left: 100px; position: relative;">' +
    // '<span class="omnidb__welcome__loading"></span>' +
    '<span class="omnidb__welcome__loading" style="background: none;">' + v_animated_omnis + '</span>' +
    '<span class="omnidb__welcome__intro-text">Hi, welcome to <span style="color:#4a6cbb;">OmniDB!</span></span>' +
  '</h1>' +
  '<div class="card p-3 omnidb__welcome__intro-card">' +
    '<p class="text-center"><span class="badge badge-danger" style="vertical-align: middle;">disclaimer</span> OmniDB is a powerful tool, and with great power...<br/>Please <strong><span class="text-danger">learn how to use it on a testing environment, NOT on production</span></strong>!</p>' +
    '<div class="text-center my-4">' +
      '<h3>' +
        '<i class="fas fa-list mr-2"></i>' +
        'Getting started' +
      '</h3>' +
    '</div>' +
    '<ol>' +
      '<li>' +
        '<button type="button" class="btn btn-lg omnidb__theme__btn--primary" onclick="startTutorial(\'utilities_menu\');">' +
          '<i class="fas fa-user-plus mr-2"></i>' +
          'Create the first omnidb user' +
        '</button>' +
      '</li>' +
    '</ol>' +
    '<div class="alert-info p-2 rounded mt-4" style="display: grid; grid-template: \'icon text\';">' +
      '<i class="fas fa-exclamation-triangle p-4" style="grid-area: icon;"></i>' +
      '<div style="grid-area: text;">' +
        `
        Our focus is to provide a very flexible, secure and work-effective environment for multiple DBMS.<br>
        With that in mind, you should <strong>be aware the many actions on the UI can lead to a direct interaction with the database</strong> that you are connected with.</br>
        ` +
      '</div>' +
    '</div>' +
  '</div>';
  // Usel links html string
  let v_html_useful_links =
  '<div class="alert alert-success p-3 omnidb__welcome__useful-card">' +
    '<h2 class="text-center mb-4">Useful stuff</h2>' +
    '<ul>' +
      '<li class="mb-2"><a class="btn btn-success text-white" target="_blank" href="https://omnidb.org"><i class="fas fa-user"></i> <span>OmniDB website</span></a></li>' +
      '<li class="mb-2"><a class="btn btn-success text-white" target="_blank" href="https://github.com/OmniDB/OmniDB"><i class="fab fa-github"></i> <span>Github repo</span></a></li>' +
      '<li><a class="btn btn-success text-white" target="_blank" href="https://omnidb.readthedocs.io/"><i class="fas fa-list"></i> <span>Read the docs</span></a></li>' +
    '</ul>' +
  '</div>';
  // Template html string
  var v_html =
  '<div class="container" style="position: relative;">' +
    '<div class="row">' +
      '<div class="col-12">' +

        // Welcome main block
        '<div id="' + v_tab.id + '_welcome" class="omnidb__welcome" style="height: 100vh;display: flex;align-items: center;font-size: 1.2rem;justify-content: center;">' +
          // Welcome grid
          '<div style="display: grid; grid-template: \'intro links\'; grid-gap: 64px;">' +
            // Intro area
            '<div style="grid-area: intro;">' +
              v_html_intro +
            '</div>' +
            // Links area
            '<div style="grid-area: links;">' +
              v_html_useful_links +
            '</div>' +
          '</div>' +
        '</div>' +

    '</div>' +//.row

  '</div>';

  v_tab.elementDiv.innerHTML = v_html;

  var v_tag = {
    tab_id: v_tab.id,
    divWelcome: document.getElementById(v_tab.id + '_welcome'),
    selectedDatabaseIndex: 0,
    connTabControl: v_connTabControl,
    mode: 'welcome'
  };

  v_tab.tag = v_tag;

  // Creating `Add` tab in the outer tab list
  v_connTabControl.tag.createAddTab();

  $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips

  endLoading();

}
