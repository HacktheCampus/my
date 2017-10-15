var inputBox;

function first_run() {
	list = ["RG", "Identidade da Universidade", "Notebook", "Carregadores", "Caderno e Caneta", "Travesseiro", "Saco de Dormir", "Escova/Pasta de Dente"]
	for (item in list)
		addItem(list[item]);
	saveList();
}

function addItem(item) {

	$('#list').append('<div class="me-want item to-do panel-body"><i class="icon minus middle aligned" aria-hidden="true" /><div class="content header">' + item + '</div></div>');

	var it = $('.me-want');
	it.fadeOut(0);
	it.fadeIn(300);
	it.removeClass('me-want');
	it.hover(addRemoveIcon, addRemoveIcon);

}

function saveList() {

	var list = [];

	$('.to-do').each(function() { list.push($(this).text()) });
	var cookie = list.join(', ');
	cookie = cookie.substring(0, cookie.length);
	Cookies.set('list', cookie, { expires: 90 });

}

function loadList() {

	var items = Cookies.get('list');

	if(items === undefined)
	{
		first_run();
		return;
	}
	if (items === '')
		return;


	items = items.split(', ');

	for (i in items) {
		addItem(items[i]);
	}

}

function add() {

	if (inputBox.val() == '') {
		return;
	}


	addItem(inputBox.val());
	inputBox.val('');

	saveList();

}

function remove(element) {

	var item = $(this);

	item.find('i').removeClass("icon middle aligned trash");
	item.find('i').removeClass("text-warning");
	item.find('i').addClass("icon middle aligned check");
	item.fadeOut(300, function() {
		item.remove();
		saveList();
	});

}

function clear() {

	var items = $('.to-do');
	var glyph = items.find('i');

	glyph.removeClass('icon middle aligned minus');
	glyph.addClass('icon middle aligned check');
	items.fadeOut(300, function() {
		items.remove();
		saveList();
	});

}

function addRemoveIcon() {

	var glyph =$(this).find('i');

	if (glyph.hasClass('icon middle aligned check'))
		return;

	glyph.toggleClass('icon middle aligned minus');
	glyph.toggleClass('icon middle aligned trash');
	glyph.toggleClass('text-warning');

}

function onKeyPress(event) {

	if (event.keyCode == 13)
		add();

}

$(document).ready(function() {

	inputBox = $('input[name="add-to-list"]');

	$('#add').click(add);
	$('#clear').click(clear);
	inputBox.keypress(onKeyPress);
	$('#list').on('click', '.to-do', remove);

	loadList();
	$('#script-error').remove();

});
