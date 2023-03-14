$(document).ready(function() {
    $('.js-example-basic-multiple').select2();
});

$(function () {
    $(".clusterpress").on("click", function() {
        var visibleObj = $('.mainSection div:visible');
        var inVisibleObj = $('.clusterPanel');
        visibleObj.fadeOut(500, function() {
            inVisibleObj.fadeIn(500);
        });
    });
    $(".transcriptpress").on("click", function() {
      var visibleObj = $('.mainSection div:visible');
      var inVisibleObj = $('.transcriptPanel');
      visibleObj.fadeOut(500, function() {
        inVisibleObj.fadeIn(500);
      });
    });
    $(".pseudotimepress").on("click", function() {
        var visibleObj = $('.mainSection div:visible');
        var inVisibleObj = $('.pseudotimePanel');
        visibleObj.fadeOut(500, function() {
            inVisibleObj.fadeIn(500);
        });
    });
    $(".genepress").on("click", function() {
        var visibleObj = $('.mainSection div:visible');
        var inVisibleObj = $('.genePanel');
        visibleObj.fadeOut(500, function() {
            inVisibleObj.fadeIn(500);
        });
    });
    $(".imputedpress").on("click", function() {
        var visibleObj = $('.mainSection div:visible');
        var inVisibleObj = $('.imputedPanel');
        visibleObj.fadeOut(500, function() {
            inVisibleObj.fadeIn(500);
        });
    });
    $(".motifpress").on("click", function() {
        var visibleObj = $('.mainSection div:visible');
        var inVisibleObj = $('.motifPanel');
        visibleObj.fadeOut(500, function() {
            inVisibleObj.fadeIn(500);
        });
    });
  });