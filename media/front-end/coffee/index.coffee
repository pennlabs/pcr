###
DOCUMENT READY
###
(->
  $(document).ready ->
    callback = undefined

    callback = ->
      $('#searchbox').autocomplete 'enable'
      $('#loading-container').hide()
      $('#searchbox').autocomplete 'search'

    $('#searchbox').live 'paste', (e) ->
      element = undefined
      text = undefined
      element = this
      setTimeout ->
      text = $(element).val()
      $('#loading-container').show()
      return init_search_box('', callback, text, true)
    , 100

    $('#searchbox').keypress ->
      setTimeout (->
        if $('#searchbox').val().length == 2
          $('#loading-container').show()
          return init_search_box('', callback, $('#searchbox').val(), true)
        else if $('#searchbox').val().length < 2
          return $('#searchbox').autocomplete('disable')
        return
      ), 10
    return
  return
).call this
