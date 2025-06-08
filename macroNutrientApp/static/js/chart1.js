const ctx = document.getElementById('nutritional-chart').getContext('2d');
        const nutritionalChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Protein', 'Carbohydrates', 'Fats'],
                datasets: [{
                    label: 'Macronutrients',
                    data: [0, 0, 0], // Initial data
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(255, 99, 132, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                }
            }
        });

        // Function to update the chart data
        function updateNutritionalChart(protein, carbs, fats) {
            nutritionalChart.data.datasets[0].data = [protein, carbs, fats];
            nutritionalChart.update();
        }

        // Example nutritional data (you should replace this with actual data from your application)
        const nutritionalData = {
            "apple": { protein: 0.3, carbs: 25, fats: 0.2 },
            "banana": { protein: 1.3, carbs: 27, fats: 0.3 },
            // Add more food items with their nutritional values here
        };

        // Handle form submission
        document.getElementById('meal-form').addEventListener('submit', function(event) {
            event.preventDefault();
            
            const foodSearch = document.getElementById('food_search').value.toLowerCase();
            const quantity = parseFloat(document.getElementById('quantity').value);
            
            if (nutritionalData[foodSearch]) {
                const { protein, carbs, fats } = nutritionalData[foodSearch];
                const totalProtein = protein * quantity;
                const totalCarbs = carbs * quantity;
                const totalFats = fats * quantity;

                updateNutritionalChart(totalProtein, totalCarbs, totalFats);
            } else {
                alert("Food item not found in the database.");
            }
        });