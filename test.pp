class web  {
  file { '/etc/apache2':
    content => epp('apache', {
      'listen' => 80,
      'documentRoot' => '/var'
    })

  }
}