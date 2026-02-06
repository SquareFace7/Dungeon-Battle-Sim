pipeline {
    agent { label 'windows' }

    // --- התיקון נמצא כאן ---
    environment {
        PYTHONIOENCODING = 'utf-8'
    }
    // ----------------------

    parameters {
        string(name: 'PLAYER_NAME', defaultValue: 'Eliad', description: 'Name of the Hero')
        choice(name: 'HERO_CLASS', choices: ['Warrior', 'Mage', 'Rogue'], description: 'Choose your class')
        string(name: 'LEVEL', defaultValue: '10', description: 'Hero Level (1-100)')
        booleanParam(name: 'HARDCORE_MODE', defaultValue: false, description: 'Enable Hardcore Mode?')
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                echo 'Code successfully pulled from GitHub.'
            }
        }

        stage('Install Requirements') {
            steps {
                echo 'Installing dependencies...'
                // השינוי שעשינו קודם נשאר כאן
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Game Simulation') {
            steps {
                script {
                    def date = new Date().format("yyyy-MM-dd")
                    echo "Starting battle for: ${params.PLAYER_NAME}..."
                    
                    bat "python dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\""
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.html, *.txt', allowEmptyArchive: true
            echo 'Battle report archived!'
        }
    }
}
