% rebase('base.tpl')
<div class="wrapper">
<h1>{{title}}</h1>
<ul>
% for record in records:
    <li>{{record.artist}} - {{record.album}} - {{record.year}} - {{record.genre}}</li>
% end
</ul>
</div>