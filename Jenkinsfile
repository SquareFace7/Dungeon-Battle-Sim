pipeline {
    agent any

    environment {
        PYTHONIOENCODING = 'utf-8'
    }

    parameters {
        choice(name: 'EXECUTOR_NODE', choices: ['windows', 'linux'], description: 'Select the machine to run on')
        string(name: 'PLAYER_NAME', defaultValue: 'Eliad', description: 'Name of the Hero')
        choice(name: 'HERO_CLASS', choices: ['Warrior', 'Mage', 'Rogue'], description: 'Choose your class')
        string(name: 'LEVEL', defaultValue: '10', description: 'Hero Level (1-100)')
        booleanParam(name: 'HARDCORE_MODE', defaultValue: false, description: 'Enable Hardcore Mode?')
    }

    stages {
        stage('Game Execution') {
            agent { label "${params.EXECUTOR_NODE}" }
            
            steps {
                echo "Running on node: ${env.NODE_NAME}"
                checkout scm
                
                script {
                    if (isUnix()) {
                        sh 'pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt'
                    } else {
                        bat 'python -m pip install -r requirements.txt'
                    }
                }

                script {
                    def date = new Date().format("yyyy-MM-dd")
                    echo "Starting battle..."
                    
                    if (isUnix()) {
                        sh "python3 dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\""
                    } else {
                        bat "python dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\""
                    }
                }
            }
        }
    }

    post {
        always {
            // זה החלק החדש שיוצר את הכפתור!
            publishHTML (target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'battle_report.html',
                reportName: 'Battle Report',
                reportTitles: 'Battle Results'
            ])
        }
    }
}
