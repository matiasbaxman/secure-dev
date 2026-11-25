pipeline {
  agent any
  options { timestamps() }
  environment {
    IMAGE = 'securedev-app'
    NET   = 'securedev-net'
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps { sh 'docker build -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .' }
    }
    stage('Test') {
      steps {
        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
          sh '''
            docker run --rm --user root --entrypoint sh $IMAGE:latest -c "pip install -q pytest && python -m pytest -q tests" > pytest.txt 2>&1
            rc=$?
            cat pytest.txt
            exit $rc
          '''
        }
      }
    }
    stage('SAST + Dependencias') {
      steps {
        sh '''
          docker run --rm --user root --entrypoint sh $IMAGE:latest -c "pip install -q bandit && python -m bandit -r app.py" > bandit.txt 2>&1 || true
          docker run --rm --user root --entrypoint sh $IMAGE:latest -c "pip install -q pip-audit && python -m pip_audit -r requirements.txt" > pip-audit.txt 2>&1 || true
          cat bandit.txt pip-audit.txt
        '''
      }
    }
    stage('Deploy') {
      steps {
        sh '''
          docker rm -f securedev-app || true
          docker run -d --name securedev-app --network $NET \
            -v securedev_data:/data -p 127.0.0.1:8000:8000 $IMAGE:latest
          for i in $(seq 1 30); do
            docker exec securedev-app python -c "import urllib.request;urllib.request.urlopen('http://localhost:8000/health')" && exit 0
            sleep 2
          done
          echo "La app no levantó"; docker logs securedev-app; exit 1
        '''
      }
    }
    stage('OWASP ZAP (DAST)') {
      steps {
        sh '''
          docker rm -f zap-scan || true
          docker run --name zap-scan --network $NET --user root zaproxy/zap-stable \
            sh -c "mkdir -p /zap/wrk && zap-baseline.py -t http://securedev-app:8000 -r zap-report.html -J zap-report.json -I" || true
          docker cp zap-scan:/zap/wrk/zap-report.html . || true
          docker cp zap-scan:/zap/wrk/zap-report.json . || true
          docker rm -f zap-scan || true
        '''
      }
    }
  }
  post {
    always {
      archiveArtifacts artifacts: '*.html, *.json, *.txt', allowEmptyArchive: true
    }
  }
}
