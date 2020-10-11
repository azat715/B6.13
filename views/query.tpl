% rebase('base.tpl')
<div class="wrapper">
<h1>Запрос к базе</h1>
<form action="/artist" method="GET">
        <input type="radio" name="type" value="artist">artist<Br>
        <input type="radio" name="type" value="album">album<Br>
        <input type="radio" name="type" value="year">year<Br>
        <input type="radio" name="type" value="genre">genre<Br>
        <input type="text" name="value" placeholder="значение"><Br>
        <button type="submit">Отправить</button>
        </form>
</div>
