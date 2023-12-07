# sets up your web servers for the deployment of web_static
exec { 'update':
command     => 'apt update',
provider    => shell,
refreshonly => true,
}

package { 'nginx':
ensure  => installed,
require => Exec['update'],
}

file { ['/data', '/data/web_static', '/data/web_static/releases',
'/data/web_static/shared', '/data/web_static/releases/test']:
ensure => directory,
}
-> file { '/data/web_static/releases/test/index.html':
ensure  => file,
content => "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
}
-> file { '/data/web_static/current':
ensure => link,
target => '/data/web_static/releases/test'
}
-> exec { 'chown -R ubuntu:ubuntu /data/':
provider => shell,
}
-> file { ['/var/www', '/var/www/html']:
ensure => directory,
}
-> file { 'var/www/html/index.html':
ensure  => file,
content => "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
}

exec{ 'config':
require  => Package['nginx'],
command  => 'sed -i "23i location /hbnb_static {\n\talias /data/web_static/current;\n\t}\n" /etc/nginx/sites-enabled/default',
provider => shell,
}
-> service { 'nginx':
ensure  => running,
}
