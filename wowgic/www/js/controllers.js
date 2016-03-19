angular.module('starter.controllers', ['ngCordova', 'angularMoment'])

.controller('fbCtrl', function($scope, $cordovaFacebook, $state, fbService, $timeout, $window, $http) {
     var browser;
    if(!$window.orientation) {
      browser = true;
    }
    else {
      browser = false;
    }

    if(localStorage.getItem("userid") && localStorage.getItem("userid")!='null'){
      $state.go("app.feeds");
    }

    $scope.fbsignin = function() {

        $cordovaFacebook.login(["public_profile", "email", "user_friends","user_photos","user_status","user_education_history","user_hometown","user_location","user_tagged_places","user_work_history","user_likes"])
            .then(function(userdetails) {
               $scope.fbuserdetails();
            
            }, function(error) {     
              console.log('errorfb', error);
              $cordovaFacebook.login(["public_profile", "email", "user_friends","user_photos","user_status","user_education_history","user_hometown","user_location","user_tagged_places","user_work_history","user_likes"])
              .then(function(userdetails) {
                $scope.fbuserdetails();
              });
            });
    }

    $scope.fbuserdetails = function() {
      $cordovaFacebook.api("/me?fields=id,name,hometown,location,education,work", ["user_friends"])
        .then(function(userdata) {
          localStorage.setItem("userid", userdata.id);          
          fbService.setData(userdata);
          $state.go("app.feeds");
        }, function(error) {
            console.log(error);
            $scope.fbsignin();
        //    $state.go("facebook");
        });
    }
})

.service('fbService', ['$cordovaFacebook', function() {
//  var response = {"id": 435354545454, "name":"chellad"};
  var response = null;
  var setData = function(userdata) {
    response = userdata;
  };

  var getData = function() {
    return response;
  }

  return {
    setData: setData,
    getData: getData
  };

}])

.filter('getById', function() {
  return function(input, id) {
    console.log('input ',input);

    var i=0, len= input.length;
    for (; i<len; i++) {
      if (input[i].id == id) {
        return input[i];
      }
    }
    return null;
  }
})
.factory('dataFactory', ['$http','$window', function($http, $window) {

  var browser = false;
  if(!$window.orientation) {
    browser = true;
  }
    //var urlBase = 'http://wowgicflaskapp-wowgic.rhcloud.com';
    var urlBase = 'http://52.36.56.217:8080';
    var dataFactory = {};
    var code = '0a1932b22820439b95511e581c4fd8e4';

    dataFactory.wowgicLogin = function (data) {
      if(browser){
        return $http.get(urlBase+'/FBLogin');
      }
      else{
      return $http.post(urlBase+'/FBLogin',data);
      }
    };
    
    /*2nd time user*/
    dataFactory.fetchAllfeeds = function (data) {
      var id = localStorage.getItem('userid');

        return $http.get(urlBase+'/refreshUserFeeds?id='+id);      
    };

    dataFactory.login = function (place) {
        return $http.get(urlBase+'/insta/login.php?code='+code+'&place='+place); 
    };

    dataFactory.renewoath = function () {
        return $http.post(urlBase+'/renewAuth',{password:localStorage.getItem('wowgicpassword')}); 
    };

    dataFactory.location = function (lat,lng) {
      return $http.get(urlBase+'/insta/login.php?code='+code+'&lat='+lat+'&long='+lng); 
    };  

    dataFactory.getNearby = function (lat,lng, radius) {
      data= {     
            "lat": lat,
            "lng": lng,
            "distance":radius
      }
      return $http.post(urlBase+'/locationFeeds',data); 
    };
    return dataFactory; 

}])

/* may be re-used
.filter('datetime', function($filter) {
  return function(input) {
    if(input == null){ 
      return ""; 
    } 
  var _date = $filter('date')(new Date(input),'MMM dd yyyy - HH:mm:ss');
  return _date.toUpperCase();
 };

})*/

.controller('settingsCtrl', function($scope,$state) {
  $scope.logout = function(){
    localStorage.setItem('userid',null);
    $scope.feeds = null;
    $state.go('facebook');
  }
})
.controller('AppCtrl', function($scope, $ionicModal, $timeout, dataFactory, fbService, $filter, $state, $ionicLoading, $http) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  // Form data for the login modal
  $scope.feeds = [];
  $scope.errorjs = false;
  var data = fbService.getData();
  var feeds;

  $scope.fetchAllfeeds = function () {
    alert('in fettch all feeds');
    $state.go("app.feeds");
    dataFactory.fetchAllfeeds().success(function(resp) {
    feeds = resp;
    angular.forEach(resp, function(key, value) {
        
        if(key.created_at) {

          $scope.parseTwitter(key)
          console.log(key.created_at);
        }
        else {
          $scope.parseInstagram(key);
        }
      
      });
    $ionicLoading.hide();
    
    if(!feeds.length) {
      $scope.errorjs = 'No feeds this time :( try later';
    }

    }).error(function(error,status,thrown) {
      $ionicLoading.hide();
      $scope.errorjs = error.textStatus;
      switch(status) {
        case 503:
          $scope.errorjs = "we're under maintanance. try after sometime";
        break;
        case 500:
          $scope.errorjs = "Something went wrong. try later";
        break;
        case 401:
          $scope.errorjs = "Sorry!! your not authorized to view this page";
        break;
      }
    });
  }

$scope.loginWowgic = function () {
    dataFactory.wowgicLogin(fbService.getData()).success(function(resp) {
    feeds = resp;
    localStorage.setItem('wowgicpassword',resp.password);
    localStorage.setItem('wowgictoken',resp.Authorization);
    
    $http.defaults.headers.common.Authorization = resp.Authorization;
    $scope.fetchAllfeeds();
    }).error(function(error) {
      $ionicLoading.hide();
      $scope.errorjs = error.textStatus;
      switch(status) {
        case 503:
          $scope.errorjs = "we're under maintanance. try after sometime";
        break;
        case 500:
          $scope.errorjs = "Something went wrong. try later";
        break;
        case 401:
          $scope.errorjs = "Sorry!! your not authorized to view this page";
        break;
      }
    });
} 
$ionicLoading.show({
      template: 'Wowing...'
    }); 

renewoath = function() {
  dataFactory.renewoath().success(function(resp) {
    $http.defaults.headers.common.Authorization = resp.Authorization;
  })
}


  if(data) {
    //first time user
    $scope.loginWowgic();  
  }
  else {
    $scope.loginWowgic();  
    renewoath();
  }


  $scope.gotoprofile = function(id) {

      var singlefeed = $filter('getById')(feeds, id);
      console.log('singlefeed',singlefeed);
      if(singlefeed.created_time) {
        //INSTAGRAM
        $scope.profile_image = singlefeed.user.profile_picture;
        $scope.showdetails = false;
        $scope.name = singlefeed.user.full_name;
        $scope.source = "instagram";

      }
      else {
      //TWITTER
      $scope.profile_image = singlefeed.user.profile_image_url;
      $scope.followers = singlefeed.user.followers_count;
      $scope.following = singlefeed.user.friends_count;
      $scope.description = singlefeed.user.description;
      $scope.name = singlefeed.user.name;
      $scope.source = "twitter";
      $scope.showdetails = true;
    }
  }

  $scope.getNearby = function () {
    $ionicLoading.show({template: 'fetching Location'}); 
    $state.go("app.feeds");
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition($scope.showPosition, $scope.showError);
    }
    else {
      $ionicLoading.hide();
      $scope.error = "Geolocation is not supported by this browser.";
    }
  }
$scope.data = {
    radius:5
};
  $scope.showPosition = function (position) {

    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    $ionicLoading.show({template: 'fetching nearby news'}); 
    $scope.$apply();
    dataFactory.getNearby(lat,lng,$scope.data.radius).success(function(resp) { 
    feeds = resp;
    $scope.feeds=[];
    angular.forEach(resp, function(key, value) {

        if(key.created_at) {

          $scope.parseTwitter(key)
          console.log(key.created_at);
        }
        else {
          $scope.parseInstagram(key)
        }
    });
    $ionicLoading.hide();
    }).error(function(error){ 
    });
  }

  $scope.showError = function (error) {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        $scope.error = "User denied the request for Geolocation."
      break;
      case error.POSITION_UNAVAILABLE:
        $scope.error = "Location information is unavailable."
      break;
      case error.TIMEOUT:
        $scope.error = "The request to get user location timed out."
      break;
      case error.UNKNOWN_ERROR:
        $scope.error = "An unknown error occurred."
      break;
    }
    alert($scope.error);
    $ionicLoading.hide();
    console.log($scope.error);
    $scope.$apply();
  }

  $scope.parseTwitter = function(obj) {
    var fata= {};
    fata.id = obj.id;
    fata.time =  obj.created_at;
    fata.text = obj.text;
    fata.user= {};
    fata.user.name = obj.user.screen_name;
    fata.image =  obj.entities.media ? obj.entities.media[0].media_url : null;
    fata.user.profile_image = obj.user.profile_image_url;
    fata.location = obj.place? obj.place.name : null;
    $scope.feeds.push(fata);
    console.log($scope.feeds);
  }

  $scope.parseInstagram= function(obj) {
    console.log('obj',obj);
    var fata= {};
      if(obj.id) {
        fata.id = obj.id;
        fata.time =  new Date(parseInt(obj.created_time) * 1000);
        fata.text = obj.caption ? obj.caption.text : null;
        fata.user= {};
        fata.image = obj.images.standard_resolution.url;
        fata.user.name = obj.user.username;
        fata.user.profile_image = obj.user.profile_picture;
        fata.location = obj.location ? obj.location.name : null;
        $scope.feeds.push(fata);
        console.log($scope.feeds);
    }
  }


  $scope.findPost = function (id, action) {
    dataFactory.login($scope.data.place).success(function(resp) {   
    $scope.items = resp;
    }).error(function(error){
    console.log('error' + error);
    });

    dataFactory.getTwitter($scope.data.place).success(function(resp) {
    console.log('twitter',resp);   
    $scope.tweets = resp.statuses;
    }).error(function(error){ 
    });
  
  }

  $scope.loginData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    // Simulate a login delay. Remove this and replace with your login
    // code if using a login system
    $timeout(function() {
      $scope.closeLogin();
    }, 1000);
  };
})

.controller('feedsCtrl', function($scope) {
  $scope.feeds1 = [
    { text: 'ReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggaeReggae hello hello hello', id: 1 },
    { text: 'Chill', id: 2 },
    { text: 'Dubstep', id: 3 },
    { text: 'Indie', id: 4 },
    { text: 'Rap', id: 5 },
    { text: 'Cowbell', id: 6 }
  ];
})

.controller('profileCtrl', function($scope, $state, $stateParams) {

  $scope.profiletitle =  $stateParams.profileid;
});

moment.locale('en', {
    relativeTime : {
        future: "in %s",
        past:   "%s",
        s:  "sec",
        m:  "1m",
        mm: "%dm",
        h:  "1h",
        hh: "%dh",
        d:  "1d",
        dd: "%dd",
        M:  "1m",
        MM: "%dm",
        y:  "1yr",
        yy: "%dyrs"
    }
})
