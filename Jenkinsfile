pipeline {
  agent { label 'mfw' }

  environment {
    lib = 'musl'
    startClean = '0'
    makeOptions = '-j32'
  }

  stages {
    stage('Build') {
      parallel {
        stage('Build x86_64') {
          environment {
            device = 'x86_64'
            dir = '/tmp/mfw-x86_64'
          }

	  stages {
            stage('Prepare workspace') {
              steps {
                sh 'cp -r . $dir'
              }
            }

            stage('Build OpenWrt') {
              steps {
                sh 'cd docker-compose -f $dir/mfw/docker-compose.build.yml -p mfw_${device} run build -d ${device} -l ${lib} -c ${startClean} -m "${makeOptions}"'
              }
            }
          }
        }

        stage('Build wrt3200') {
          environment {
            device = 'wrt3200'
            dir = '/tmp/mfw-wrt3200'
          }

	  stages {
            stage('Prepare workspace') {
              steps {
                sh 'cp -r . $dir'
              }
            }

            stage('Build OpenWrt') {
              steps {
                sh 'cd docker-compose -f $dir/mfw/docker-compose.build.yml -p mfw_${device} run build -d ${device} -l ${lib} -c ${startClean} -m "${makeOptions}"'
              }
            }
          }
        }

        stage('Build wrt1900') {
          environment {
            device = 'wrt1900'
            dir = '/tmp/mfw-wrt1900'
          }

	  stages {
            stage('Prepare workspace') {
              steps {
                sh 'cp -r . $dir'
              }
            }

            stage('Build OpenWrt') {
              steps {
                sh 'cd docker-compose -f $dir/mfw/docker-compose.build.yml -p mfw_${device} run build -d ${device} -l ${lib} -c ${startClean} -m "${makeOptions}"'
              }
            }
          }
        }

        stage('Build omnia') {
          environment {
            device = 'omnia'
            dir = '/tmp/mfw-omnia'
          }

	  stages {
            stage('Prepare workspace') {
              steps {
                sh 'cp -r . $dir'
              }
            }

            stage('Build OpenWrt') {
              steps {
                sh 'cd docker-compose -f $dir/mfw/docker-compose.build.yml -p mfw_${device} run build -d ${device} -l ${lib} -c ${startClean} -m "${makeOptions}"'
              }
            }
          }
        }

      }
    }
  }
}
