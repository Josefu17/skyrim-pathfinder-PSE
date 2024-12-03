// Run tests and collect coverage
mocha.run(() => {
    // Collect coverage
    if (window.__coverage__) {
        console.log('Coverage data:', window.__coverage__);

        // Use Istanbul to generate an HTML report
        const coverage = window.__coverage__;
        const coverageMap = new window.IstanbulLibCoverage.CoverageMap();
        coverageMap.addFileCoverage(coverage);

        // Create the reporter and output the report
        const reporter = window.IstanbulReports.create('html');
        reporter.write(coverageMap);
        alert('Coverage data has been collected! Check console and coverage report.');
    } else {
        console.warn('No coverage data collected!');
    }
});
