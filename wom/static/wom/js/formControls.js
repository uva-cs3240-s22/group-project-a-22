function cloneMore(selector, prefix) {
  var newElement = $(selector + ":last").clone(true);
  var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
  var elementId = $(selector + ":first").find("#id_" + prefix + "-0-id").val();
  console.log(elementId);
  newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
    var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total +'-');
    var id = 'id_' + name;
    $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
  });
  newElement.find('label').each(function() {
    var forValue = $(this).attr('for');
    if (forValue) {
      forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
      $(this).attr({'for': forValue});
    }
  });
  newElement.find('#id_' + prefix + '-' + total + '-id').val(elementId);
  total++;
  $('#id_' + prefix + '-TOTAL_FORMS').val(total);
  $(selector + ":last").after(newElement);
  return false;
}

function updateElementIndex(element, prefix, index) {
  var id_regex = new RegExp('(' + prefix + '-\\d+)');
  var replacement = prefix + '-' + index;
  if ($(element).attr('for')) {
    $(element).attr('for', $(element).attr("for").replace(id_regex, replacement));
  }

  if (element.id) {
    element.id = element.id.replace(id_regex, replacement);
  }

  if (element.name) {
    element.name = element.name.replace(id_regex, replacement);
  }
}

function deleteForm(prefix, btn) {
  var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
  if (total > 1) {
    btn.closest('.' + prefix + '-form').remove();
    // btn.closest('.' + prefix + '-form').css("display","none");
    // btn.prev().find('.form-check-input').attr("checked", true);
    var forms = $('.' + prefix + '-form');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i = 0, formCount=forms.length; i < formCount; i++) {
      $(forms.get(i)).find(':input').each(function() {
        updateElementIndex(this, prefix, i);
      });
    }
  }
  return false;
}

function disableField(field_id, form_id) {
  document.getElementById(field_id).disabled = true;
  document.getElementById(form_id).submit();
}