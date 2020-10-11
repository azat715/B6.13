% rebase('base.tpl')
<div class="wrapper">
<h1>Создание артиста</h1>
<form action="/new_artist" enctype="application/x-www-form-urlencoded" method="POST">
        <input type="text" name="artist" placeholder="artist"><Br>
        <input type="text" name="album" placeholder="album"><Br>
        <input type="text" name="year" placeholder="year"><Br>
        <input type="text" name="genre" placeholder="genre"><Br>
        <button type="submit">Создать</button>
        </form>
</div>
