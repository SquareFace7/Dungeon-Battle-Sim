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
        // --- שלב חדש: ניקוי שולחן ---
        stage('Clean Workspace') {
            agent { label "${params.EXECUTOR_NODE}" }
            steps {
                echo "Cleaning workspace..."
                cleanWs() // מוחק הכל! מבטיח שלא יישארו קבצים ישנים
            }
        }
        
        stage('Checkout Code') {
            agent { label "${params.EXECUTOR_NODE}" }
            steps {
                echo "Running on node: ${env.NODE_NAME}"
                checkout scm
            }
        }

        stage('Validate Parameters') {
            agent { label "${params.EXECUTOR_NODE}" }
            steps {
                script {
                    echo "Validating inputs..."
                    if (params.LEVEL.toInteger() < 1 || params.LEVEL.toInteger() > 100) {
                        error "Level must be between 1 and 100!"
                    }
                    echo "Parameters are valid: ${params.PLAYER_NAME}"
                }
            }
        }

        stage('Install Requirements') {
            agent { label "${params.EXECUTOR_NODE}" }
            steps {
                 script {
                    echo "Installing dependencies..."
                    if (isUnix()) {
                        sh 'pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt'
                    } else {
                        bat 'python -m pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Run Script & Generate HTML') {
            agent { label "${params.EXECUTOR_NODE}" }
            steps {
                script {
                    def date = new Date().format("yyyy-MM-dd")
                    def hardcoreFlag = params.HARDCORE_MODE ? '--hardcore_mode' : ''
                    
                    echo "Starting battle simulation for ${params.PLAYER_NAME}..."
                    
                    // מחיקה כפויה של הדוח הישן (ליתר ביטחון)
                    if (isUnix()) {
                        sh "rm -f battle_report.html" 
                        sh "python3 dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\" ${hardcoreFlag}"
                    } else {
                        bat "if exist battle_report.html del battle_report.html"
                        bat "python dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\" ${hardcoreFlag}"
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.html, *.txt, *.css', allowEmptyArchive: true
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
