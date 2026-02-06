pipeline {
    agent { label 'windows' }  // מוודא שזה ירוץ על המחשב שלך

    parameters {
        string(name: 'PLAYER_NAME', defaultValue: 'Eliad', description: 'Name of the Hero')
        choice(name: 'HERO_CLASS', choices: ['Warrior', 'Mage', 'Rogue'], description: 'Choose your class')
        string(name: 'LEVEL', defaultValue: '10', description: 'Hero Level (1-100)')
        booleanParam(name: 'HARDCORE_MODE', defaultValue: false, description: 'Enable Hardcore Mode?')
    }

    stages {
        stage('Checkout') {
            steps {
                // ג'נקינס מוריד את הקוד אוטומטית
                checkout scm
            }
        }

        stage('Install Requirements') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Game Simulation') {
            steps {
                script {
                    // יצירת תאריך אוטומטי
                    def date = new Date().format("yyyy-MM-dd")
                    echo "Running game for user: ${params.PLAYER_NAME}"
                    
                    // הרצת הסקריפט עם הפרמטרים מהמשתמש
                    bat "python dungeon_sim.py --player_name \"${params.PLAYER_NAME}\" --hero_class \"${params.HERO_CLASS}\" --level ${params.LEVEL} --battle_date \"${date}\""
                }
            }
        }
    }

    post {
        always {
            // שמירת התוצאות (HTML + Log) כדי שתוכל לראות אותן בג'נקינס
            archiveArtifacts artifacts: '*.html, *.txt', allowEmptyArchive: true
        }
    }
}
